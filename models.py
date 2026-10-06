from dataclasses import dataclass


@dataclass
class Category:
    id: int
    name: str


@dataclass
class Transaction:
    id: int
    category_id: int
    amount: int
    date: str
    description: str


@dataclass
class Budget:
    id: int
    category_id: int
    amount: int
    period: str