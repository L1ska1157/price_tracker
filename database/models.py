from sqlalchemy import (
    BigInteger,
    ForeignKey,
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
            'name': 'page__title'
    }
    allo = {
            'price': 'a-product-price__current',
            'name': 'p-view__header-title'
    }
    comfy = {
            'price': 'price__current',
            'name': 'product-title'
    },
    cytrus = {
            'price': 'price',
            'name': 'DescriptionTitle_title__PxMkv'
    }
    moyo = {
            'price': 'product_price_current',
            'name': 'product_name'
    }
    stylus = {
            'price': 'sc-7d638165-4',
            'name': 'sc-4bec5e00-0'
    }
    

class Users(Base):
    __tablename__ = 'Users'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
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
    