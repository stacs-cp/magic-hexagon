
for order in range(3, 8+1):
    for shift in range(-10, 10+1):
        with open(f"order{str(order).zfill(3)}--shift{str(shift).zfill(4)}.param", "w") as f:
            print(f"""
                  letting order be {order}
                  letting shift be {shift}""", file=f)
