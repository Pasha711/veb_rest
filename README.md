# Bean Drop API — Документація REST API інтернет-магазину кави

## Опис проєкту
«Bean Drop» — це спеціалізований інтернет-магазин свіжообсмаженої кави в зернах. Сайт дозволяє користувачам переглядати каталог кави, шукати за назвою або країною походження, фільтрувати товари за ступенем обсмажування, способом обробки та смаковими нотами, сортувати за ціною чи популярністю. Також передбачено сторінки країн походження (регіонів), кошик, швидке оформлення замовлення, особистий кабінет із переглядом історії замовлень та адмін-панель для управління асортиментом.

---

## Ендпоінти REST API (JSON)

### 1. Кава (Coffees / Products)
* **`GET /api/coffees`**
  * **Опис:** Отримання списку всіх видів кави з підтримкою пошуку, фільтрації та сортування.
  * **Query Parameters:** 
    * `search` (пошук за назвою)
    * `origin_id` (фільтр за країною походження)
    * `roast_level` (фільтр за обсмажуванням: `light`, `medium`, `dark`)
    * `processing` (фільтр за обробкою: `washed`, `natural`, `honey`)
    * `sort_by` (`price_asc`, `price_desc`, `popularity`)
  * **Response Status:** `200 OK`
  * **Response Body (JSON):**
    ```json
    [
      {
        "id": 1,
        "title": "Ethiopia Yirgacheffe",
        "price": 420.00,
        "weight_grams": 250,
        "roast_level": "light",
        "processing_method": "washed",
        "flavor_notes": "Bergamot, Jasmine, Peach",
        "origin": "Ethiopia",
        "popularity": 98
      }
    ]
    ```

* **`GET /api/coffees/{id}`**
  * **Опис:** Отримання детальної інформації про конкретний вид кави (з рекомендаціями щодо заварювання).
  * **Response Status:** `200 OK` / `404 Not Found`

* **`POST /api/coffees`** *(Admin)*
  * **Опис:** Додавання нового позиції кави до каталогу.
  * **Request Body:** `{ "title": "...", "description": "...", "price": ..., "weight_grams": 250, "roast_level": "...", "processing_method": "...", "flavor_notes": "...", "origin_id": ..., "stock_quantity": ... }`
  * **Response Status:** `201 Created`

* **`PUT /api/coffees/{id}`** *(Admin)* — Оновлення даних товару.
* **`DELETE /api/coffees/{id}`** *(Admin)* — Видалення товару з каталогу.

---

### 2. Країни походження (Origins)
* **`GET /api/origins`** — Отримання списку всіх країн та регіонів походження зерна.
* **`GET /api/origins/{id}`** — Сторінка регіону разом зі списком доступної звідти кави.
* **`POST /api/origins`** *(Admin)* — Додати новий регіон.

---

### 3. Авторизація та профіль (Auth & Profile)
* **`POST /api/auth/register`**
  * **Request Body:** `{ "username": "...", "email": "...", "password": "..." }`
  * **Response Status:** `201 Created`
* **`POST /api/auth/login`**
  * **Request Body:** `{ "email": "...", "password": "..." }`
  * **Response Status:** `200 OK`
* **`GET /api/profile`** *(Auth)* — Отримання даних поточного користувача.
* **`PUT /api/profile`** *(Auth)* — Редагування особистих даних.

---

### 4. Кошик (Cart)
* **`GET /api/cart`** *(Auth)* — Перегляд вмісту кошика.
* **`POST /api/cart/items`** *(Auth)*
  * **Request Body:** `{ "coffee_id": 1, "quantity": 2 }`
  * **Response Status:** `200 OK`
* **`DELETE /api/cart/items/{id}`** *(Auth)* — Видалення позиції з кошика.

---

### 5. Замовлення (Orders)
* **`POST /api/orders`** *(Auth)*
  * **Опис:** Швидке створення замовлення на основі поточного кошика.
  * **Response Status:** `201 Created`
* **`GET /api/orders`** *(Auth)* — Історія замовлень користувача.

---

### 6. Інформація (Information)
* **`GET /api/about`**
  * **Опис:** Контакти кав'ярні/магазину, умови доставки та повернення кавових зернят.

---

## Схема бази даних
<img width="882" height="1012" alt="_DB_schema drawio" src="https://github.com/user-attachments/assets/9abf6d69-419c-4d3d-9a3d-655e6a7c7d67" />
