# GameHub — Django Gaming Console Store

A full-featured e-commerce website built with Django, styled after PlayStation/Xbox-style
storefronts, for selling gaming consoles, controllers, headsets, accessories and games.

## Features

- **Catalog**: Consoles, Controllers, Headsets, Accessories, and Games across brands
  (Sony, Microsoft, Nintendo, Razer, Logitech, SteelSeries, Astro, 8BitDo...)
- **Product browsing**: search, category filter, brand filter, platform filter,
  price range filter, in-stock filter, sorting, pagination
- **Product detail pages**: image gallery, specs, star ratings, customer reviews
- **Cart**: works for guests (session-based) and logged-in users, auto-merges guest
  cart into account cart on login
- **Wishlist**: per-user, toggle from any product card or detail page
- **Checkout**: shipping form pre-filled from profile, stock validation, order creation
- **Order history & order detail** pages for each customer
- **Accounts**: signup, login, logout, profile editing (auto-creates a Profile via signal)
- **Reviews**: 1–5 star ratings with title/comment, one review per user per product
- **Admin panel**: manage products (with inline extra images), categories, brands,
  orders (with inline order items and status updates), reviews, users
- **Dark, gaming-store themed UI** built with Bootstrap 5 + custom CSS (no external
  build step required — everything runs from Django templates + static files)

## Requirements

- Python 3.10+
- pip

## Setup

```bash
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. (Optional) Seed the catalog with sample products
python manage.py seed_data

# 5. Create an admin account
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Then visit:
- **Storefront**: http://127.0.0.1:8000/
- **Admin panel**: http://127.0.0.1:8000/admin/

> Note: A `db.sqlite3` database is already included in this zip, pre-seeded with
> 5 categories, 9 brands, 25 products, and an admin account
> (**username:** `admin`, **password:** `Admin@12345`) so you can run the app
> immediately without seeding. Change this password before any real deployment.

## Project Structure

```
gamehub/
├── manage.py
├── requirements.txt
├── db.sqlite3                # pre-seeded sample database
├── gamehub/                  # project settings, urls
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── store/                    # main e-commerce app
│   ├── models.py             # Product, Category, Brand, Cart, Order, Review, etc.
│   ├── views.py               # all storefront views
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── cart.py                # session/user cart helpers
│   ├── signals.py             # auto-create Profile on signup
│   ├── context_processors.py  # cart count + categories in every template
│   ├── templatetags/store_extras.py
│   └── management/commands/seed_data.py
├── templates/
│   ├── base.html
│   ├── registration/          # login, signup
│   └── store/                 # home, product list/detail, cart, checkout, orders...
├── static/
│   ├── css/style.css          # dark gaming-store theme
│   └── js/, img/
└── media/products/            # sample placeholder product images
```

## Notes on Product Images

Since this project was built without internet access to license real product photos,
sample product images are simple generated placeholder graphics (colored by category)
stored in `media/products/`. Swap them out for real photos via the Admin panel — just
edit a Product and upload a new image.

## Production Checklist

Before deploying to production, be sure to:
- Set `DEBUG = False` in `gamehub/settings.py`
- Set a proper `SECRET_KEY` via environment variable
- Set `ALLOWED_HOSTS` to your real domain(s)
- Switch from SQLite to PostgreSQL/MySQL
- Configure a real email backend (currently uses the console backend)
- Serve static/media files via a proper web server or CDN (`collectstatic`)
- Add HTTPS/SSL and Django's security middleware settings
