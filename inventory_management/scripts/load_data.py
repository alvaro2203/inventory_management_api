import json
import logging
from inventory_management.models import Category, Provider, Product, StockMovement, MovementType
from inventory_management.db import get_db_context

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

JSON_FILE = "data.json"

def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"JSON cargado correctamente desde {file_path}")
        return data
    except Exception as e:
        logger.error(f"No se pudo cargar el JSON: {e}")
        raise

def upsert_category(db, c):
    c_id = int(c["id"])
    existing = db.get(Category, c_id)
    if existing:
        existing.name = c["name"]
        logger.info(f"Actualizada categoría existente: {c['name']}")
    else:
        category = Category(id=c_id, name=c["name"])
        db.add(category)
        logger.info(f"Insertada nueva categoría: {c['name']}")

def upsert_provider(db, p):
    p_id = int(p["id"])
    existing = db.get(Provider, p_id)
    if existing:
        existing.name = p["name"]
        existing.contact_email = p["contact_email"]
        logger.info(f"Actualizado proveedor existente: {p['name']}")
    else:
        provider = Provider(id=p_id, name=p["name"], contact_email=p["contact_email"])
        db.add(provider)
        logger.info(f"Insertado nuevo proveedor: {p['name']}")

def upsert_product(db, pr):
    pr_id = int(pr["id"])
    category_id = int(pr["category_id"])
    provider_id = int(pr["provider_id"]) if pr.get("provider_id") else None

    if not db.get(Category, category_id):
        logger.warning(f"Producto {pr['name']} no insertado: categoría {category_id} no existe")
        return

    if provider_id and not db.get(Provider, provider_id):
        logger.warning(f"Producto {pr['name']} no insertado: proveedor {provider_id} no existe")
        return

    existing = db.get(Product, pr_id)
    if existing:
        existing.name = pr["name"]
        existing.category_id = category_id
        existing.provider_id = provider_id
        logger.info(f"Producto actualizado: {pr['name']}")
    else:
        product = Product(
            id=pr_id,
            name=pr["name"],
            category_id=category_id,
            provider_id=provider_id
        )
        db.add(product)
        logger.info(f"Producto insertado: {pr['name']}")

def upsert_stock_movement(db, sm):
    sm_id = int(sm["id"])
    product_id = int(sm["product_id"])

    if not db.get(Product, product_id):
        logger.warning(f"Movimiento {sm_id} no insertado: producto {product_id} no existe")
        return

    movement_data = {
        "product_id": product_id,
        "movement_type": MovementType(sm["movement_type"]),
        "quantity": sm["quantity"],
    }

    existing = db.get(StockMovement, sm_id)
    if existing:
        for k, v in movement_data.items():
            setattr(existing, k, v)
        logger.info(f"Movimiento de stock actualizado: {sm_id}")
    else:
        movement = StockMovement(id=sm_id, **movement_data)
        db.add(movement)
        logger.info(f"Movimiento de stock insertado: {sm_id}")

def main():
    data = load_json(JSON_FILE)

    with get_db_context() as db:
        for c in data.get("categories", []):
            upsert_category(db, c)
        db.flush()

        for p in data.get("providers", []):
            upsert_provider(db, p)
        db.flush()

        for pr in data.get("products", []):
            upsert_product(db, pr)
        db.flush()

        for sm in data.get("stock_movements", []):
            upsert_stock_movement(db, sm)

        try:
            db.commit()
            logger.info("Todos los cambios confirmados en la base de datos.")
        except Exception as e:
            logger.error(f"No se pudo hacer commit final: {e}")
            db.rollback()

if __name__ == "__main__":
    main()
