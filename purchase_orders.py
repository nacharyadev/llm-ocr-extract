import re
from typing import Optional
from pydantic import BaseModel, ConfigDict

class Item(BaseModel):
    itemId: Optional[str] = None
    itemName: Optional[str] = None
    itemQuantity: int
    itemPrice: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)

class PurchaseOrder(BaseModel):
    purchaseOrderNumber: str
    trackingNumber: Optional[str] = None
    date: Optional[str] = None
    customerName: Optional[str] = None
    customerAddress: Optional[str] = None
    items: list[Item] = []

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self) -> dict:
        return self.model_dump()

    def to_json(self) -> str:
        return self.model_dump_json()

    @classmethod
    def from_dict(cls, data: dict) -> 'PurchaseOrder':
        return cls.model_validate(data)

    @classmethod
    def from_json(cls, json_str: str) -> 'PurchaseOrder':
        return cls.model_validate_json(json_str)

def parse_purchase_order(text: str) -> PurchaseOrder:
    # Extract purchase order number from text
    purchase_order_number_match = re.search(r'\"purchaseOrderNumber\": \"([A-Za-z0-9-]+)\"', text)
    if purchase_order_number_match:
        return PurchaseOrder(purchaseOrderNumber=purchase_order_number_match.group(1), items=[])
    else:
        return None

class PurchaseOrderList:
    def __init__(self):
        self.purchaseOrders = [
            PurchaseOrder(
                trackingNumber="LZ92738101",
                date="March 19th, 2025",
                customerName="John Smith",
                customerAddress="605 Random Lake Rd, 53075\nRandom Lake, WI, United States",
                purchaseOrderNumber="#ORDER_571",
                items=[
                    Item(itemName="Item 1", itemQuantity=1, itemPrice=100),
                    Item(itemName="Item 2", itemQuantity=2, itemPrice=200),
                    Item(itemName="Item 3", itemQuantity=3, itemPrice=300),
                ]
            ),
            PurchaseOrder(
                trackingNumber="LZ92738102",
                date="March 20th, 2025",
                customerName="Jane Doe",
                customerAddress="123 Main St, Anytown, USA",
                purchaseOrderNumber="#ORDER_572",
                items=[
                    Item(itemName="Item 4", itemQuantity=4, itemPrice=400),
                    Item(itemName="Item 5", itemQuantity=5, itemPrice=500),
                    Item(itemName="Item 6", itemQuantity=6, itemPrice=600),
                ]
            ),
            PurchaseOrder(
                trackingNumber="LZ92738103",
                date="March 21st, 2025",
                customerName="Jim Beam",
                customerAddress="456 Maple Ave, Anytown, USA",
                purchaseOrderNumber="#ORDER_573",
                items=[
                    Item(itemName="Item 7", itemQuantity=7, itemPrice=700),
                    Item(itemName="Item 8", itemQuantity=8, itemPrice=800),
                    Item(itemName="Item 9", itemQuantity=9, itemPrice=900),
                ]
            ),
            PurchaseOrder(
                trackingNumber="LZ92738104",
                date="March 22nd, 2025",
                customerName="John Doe",
                customerAddress="789 Oak St, Anytown, USA",
                purchaseOrderNumber="#ORDER_574",
                items=[
                    Item(itemName="Item 10", itemQuantity=10, itemPrice=1000),
                    Item(itemName="Item 11", itemQuantity=11, itemPrice=1100),
                    Item(itemName="Item 12", itemQuantity=12, itemPrice=1200),
                ]
            ),
            PurchaseOrder(
                trackingNumber="LZ92738105",
                date="March 23rd, 2025",
                customerName="Jane Smith",
                customerAddress="321 Pine St, Anytown, USA",
                purchaseOrderNumber="#ORDER_575",
                items=[
                    Item(itemName="Item 13", itemQuantity=13, itemPrice=1300),
                    Item(itemName="Item 14", itemQuantity=14, itemPrice=1400),
                    Item(itemName="Item 15", itemQuantity=15, itemPrice=1500),
                ]
            ),
            PurchaseOrder(
                trackingNumber="75882988764",
                date="March 17th, 2025",
                customerName="Naveen Acharya",
                customerAddress="789 Oak St, Anytown, USA",
                purchaseOrderNumber="W1506150551",
                items=[
                    Item(itemName="Item 16", itemQuantity=16, itemPrice=1600)
                ]
            )
        ]

    def add(self, purchaseOrder: PurchaseOrder):
        self.purchaseOrders.append(purchaseOrder)

    def get_purchase_order(self, purchaseOrderNumber: str):
        print(purchaseOrderNumber)
        for purchaseOrder in self.purchaseOrders:
            if purchaseOrder.purchaseOrderNumber == purchaseOrderNumber:
                return purchaseOrder
        return None

    def get_purchase_orders(self):
        return self.purchaseOrders
