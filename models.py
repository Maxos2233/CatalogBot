from dataclasses import dataclass
from bson import ObjectId

@dataclass
class ProductEntity:
    name : str
    article : str
    quantity : int
    id : ObjectId = None

@dataclass
class ProductCreateDTO:
    name : str
    article : str
    quantity : int

@dataclass
class ProductUpdateDTO:
    article: str
    quantity : int

@dataclass
class ProductGetArticleDTO:
    article: str

@dataclass
class ProductShowDTO:
    name : str
    article : str
    quantity : int