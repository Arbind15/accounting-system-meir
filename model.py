from sqlalchemy import Column, Integer, String, Date, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class SupplierDetail(Base):
    __tablename__ = 'supplier_details'

    id = Column(Integer, primary_key=True)
    supplier_name = Column(String)
    invoice_date = Column(Date)
    invoice_type = Column(String)
    invoice_number = Column(String)
    building_name = Column(String)
    budget_type_1 = Column(String)
    budget_type_2 = Column(String)
    supplier_type = Column(String)
    account_details = Column(String)
    affiliation_period = Column(String)
    remark = Column(String)
    e1 = Column(String)
    e2 = Column(String)
    e3 = Column(String)

if __name__ == '__main__':
    # Replace 'sqlite:///example.db' with the actual database URL you want to use
    engine = create_engine('sqlite:///data.db')
    # Create the table in the database
    Base.metadata.create_all(engine)