from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    text,
    CheckConstraint,
    Index
    )
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship
                            )
from database.database import (
    Base
    )
from enum import (
    Enum
)


# *** All tables


class ShopType(Enum):
    foxtrot = {
            'price': 'product-box__main_price',
            'name': ''
    }
    allo = 'allo'
    comfy = 'comfy',
    cytrus = 'cytrus'
    moyo = 'moyo'
    stylus = 'stylus'
    

class Users(Base):
    __tablename__ = 'Users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tracked_products: Mapped[list['Products']] = relationship(
        back_populates='user'
    )
    
    def __repr__(self):
        return f'<User, id={self.id}>'
    
    
class Products(Base):
    __tablename__ = 'Products'
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            'Users.id', 
            ondelete='CASCADE'
            ),
        primary_key=True
    )
    link: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    shop: Mapped[ShopType]
    user: Mapped['Users'] = relationship(
        back_populates='tracked_products'
    )
    price_0: Mapped[int]
    price_1: Mapped[int]
    price_2: Mapped[int]
    price_3: Mapped[int]
    price_4: Mapped[int]
    price_5: Mapped[int]
    price_6: Mapped[int]
    
    __table_args__ = (
        Index('shop', 'shop'),
    )
    
    def __repr__(self):
        return f'<Product, user_id={self.user_id}, name={self.name}, shop={self.shop}, last_price={self.price_0}>'
    