from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()


class Site(db.Model):
    """考核地点"""
    __tablename__ = 'sites'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(500))
    contact_person = db.Column(db.String(100))
    contact_phone = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    inspections = db.relationship('Inspection', backref='site', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address or '',
            'contact_person': self.contact_person or '',
            'contact_phone': self.contact_phone or '',
            'description': self.description or '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
        }


class Category(db.Model):
    """考核类别"""
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    weight = db.Column(db.Float, default=1.0)
    sort_order = db.Column(db.Integer, default=0)
    criteria = db.relationship('Criteria', backref='category', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description or '',
            'weight': self.weight,
            'sort_order': self.sort_order,
            'criteria_count': self.criteria.count(),
        }


class Criteria(db.Model):
    """考核标准/考核要求点"""
    __tablename__ = 'criteria'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    max_score = db.Column(db.Float, default=100.0)
    deduction_rule = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else '',
            'name': self.name,
            'description': self.description or '',
            'max_score': self.max_score,
            'deduction_rule': self.deduction_rule or '',
            'sort_order': self.sort_order,
            'is_active': self.is_active,
        }


class Inspection(db.Model):
    """考核记录（一次现场检查）"""
    __tablename__ = 'inspections'
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)
    inspector = db.Column(db.String(100), nullable=False)
    inspection_date = db.Column(db.Date, nullable=False, default=date.today)
    total_score = db.Column(db.Float, default=100.0)
    total_deduction = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='draft')  # draft, completed, reviewed
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    items = db.relationship('InspectionItem', backref='inspection', lazy='dynamic',
                            cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'site_id': self.site_id,
            'site_name': self.site.name if self.site else '',
            'inspector': self.inspector,
            'inspection_date': self.inspection_date.strftime('%Y-%m-%d'),
            'total_score': self.total_score,
            'total_deduction': self.total_deduction,
            'status': self.status,
            'status_label': {'draft': '草稿', 'completed': '已完成', 'reviewed': '已审核'}.get(self.status, self.status),
            'notes': self.notes or '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'item_count': self.items.count(),
        }


class InspectionItem(db.Model):
    """考核明细（每个考核要求点的检查结果）"""
    __tablename__ = 'inspection_items'
    id = db.Column(db.Integer, primary_key=True)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspections.id'), nullable=False)
    criteria_id = db.Column(db.Integer, db.ForeignKey('criteria.id'), nullable=False)
    score = db.Column(db.Float, default=0.0)
    deduction = db.Column(db.Float, default=0.0)
    is_qualified = db.Column(db.Boolean, default=True)
    issue_description = db.Column(db.Text)
    rectification_status = db.Column(db.String(20), default='none')  # none, pending, completed
    notes = db.Column(db.Text)

    criteria_ref = db.relationship('Criteria', backref='inspection_items')

    def to_dict(self):
        return {
            'id': self.id,
            'inspection_id': self.inspection_id,
            'criteria_id': self.criteria_id,
            'criteria_name': self.criteria_ref.name if self.criteria_ref else '',
            'category_name': self.criteria_ref.category.name if self.criteria_ref and self.criteria_ref.category else '',
            'max_score': self.criteria_ref.max_score if self.criteria_ref else 0,
            'score': self.score,
            'deduction': self.deduction,
            'is_qualified': self.is_qualified,
            'issue_description': self.issue_description or '',
            'rectification_status': self.rectification_status,
            'rectification_label': {
                'none': '无需整改', 'pending': '待整改', 'completed': '已整改'
            }.get(self.rectification_status, self.rectification_status),
            'notes': self.notes or '',
        }
