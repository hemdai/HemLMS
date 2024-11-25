from slugify import slugify


def generate_unique_slug(cls, target_word, connection):
    """
    Generates a unique slug for a SQLAlchemy model instance.
    """
    slug = slugify(target_word)

    # Check for uniqueness
    existing = connection.execute(
        cls.__table__.select().where(cls.slug == slug)
    ).fetchone()

    if existing:
        counter = 1
        while True:
            new_slug = f"{slug}-{counter}"
            existing = connection.execute(
                cls.__table__.select().where(cls.slug == new_slug)
            ).fetchone()
            if not existing:
                slug = new_slug
                break
            counter += 1
    return slug
