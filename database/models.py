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


# *** All tables
    

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
    user: Mapped['Users'] = relationship(
        back_populates='tracked_products'
    )
    price_0: Mapped[int]
    price_1: Mapped[int | None]
    price_2: Mapped[int | None]
    price_3: Mapped[int | None]
    price_4: Mapped[int | None]
    price_5: Mapped[int | None]
    price_6: Mapped[int | None]
    
    
    def __repr__(self):
        return f'<Product, user_id={self.user_id}, name={self.name}, last_price={self.price_0}>'
    