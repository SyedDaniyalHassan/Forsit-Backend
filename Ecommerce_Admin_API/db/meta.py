import sqlalchemy as sa

from Ecommerce_Admin_API.db.models import load_all_models

# Load all models to ensure they are registered
load_all_models()

meta = sa.MetaData()
