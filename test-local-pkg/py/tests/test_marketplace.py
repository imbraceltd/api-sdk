from utils.utils import client, run_test_section, log_result

def test_marketplace():
    print("\n🚀 Testing Marketplace Resource...")

    state = {"product_id": None}

    # 1. Products — list + get_product (per method-py.md)
    def products_ops():
        res = client.marketplace.list_products()
        data = res.get("data", [])
        log_result("Products Count", len(data))
        if data:
            state["product_id"] = data[0].get("id") or data[0].get("_id")

        if state["product_id"]:
            try:
                product = client.marketplace.get_product(state["product_id"])
                log_result("Product Detail", product.get("id") or product.get("_id"))
            except Exception as e:
                print(f"   ⚠️ marketplace.get_product failed: {str(e)}")
    run_test_section("marketplace.list_products + get_product", products_ops)

    # 2. Orders
    run_test_section("marketplace.list_orders", lambda: log_result("Orders Count", len(client.marketplace.list_orders().get("data", []))))

    # 3. Misc
    run_test_section("marketplace.list_use_case_templates", lambda: log_result("UseCase Templates Count", len(client.marketplace.list_use_case_templates())))
    run_test_section("marketplace.list_categories", lambda: log_result("Categories Count", len(client.marketplace.list_categories())))

    print("\n✅ Marketplace Resource Testing Completed.")

if __name__ == "__main__":
    test_marketplace()
