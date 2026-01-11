
PRICING = {
    "bike":  {"price_per_hour": 5000,  "max_fee": 30000},
    "car":   {"price_per_hour": 10000, "max_fee": 100000},
    "truck": {"price_per_hour": 20000, "max_fee": 200000},
}
VALID_TYPES = {"bike", "car", "truck"}
PEAK_RANGES = [(7, 9), (17, 19)]
MAX_CAPACITY_Q5 = 50
# ---------- HELPERS ----------
def is_peak_hour(hour_in):
    for start, end in PEAK_RANGES:
        if start <= hour_in < end:
            return True
    return False


def calc_fee(vehicle_type, duration, hour_in=None):
    info = PRICING[vehicle_type]
    fee = duration * info["price_per_hour"]

    if hour_in is not None and is_peak_hour(hour_in):
        fee = fee * 1.2

    if fee > info["max_fee"]:
        fee = info["max_fee"]

    return int(round(fee))


def safe_float_input(prompt):
    while True:
        s = input(prompt).strip()
        try:
            return float(s)
        except:
            print("Không hợp lệ. Hãy nhập số (vd: 8 hoặc 9.5).")


def safe_int_input(prompt):
    while True:
        s = input(prompt).strip()
        try:
            return int(s)
        except:
            print("Không hợp lệ. Hãy nhập số nguyên.")
# Q1 – Parking Fee Calculator 
def question_1():
    print("\n===== Q1 – Parking Fee Calculator =====")
    print("Nhập danh sách xe trong ngày.")
    print("Cú pháp mỗi xe: vehicle_id vehicle_type hours_parked")
    print("Ví dụ: A01 car 12")
    print("Gõ STOP để kết thúc nhập.\n")

    fees = {}
    total_revenue = 0
    count_by_type = {"bike": 0, "car": 0, "truck": 0}

    while True:
        line = input("Nhập xe (hoặc STOP): ").strip()
        if line.upper() == "STOP":
            break

        parts = line.split()
        if len(parts) != 3:
            print("Sai cú pháp. Ví dụ đúng: A01 car 12")
            continue

        vehicle_id = parts[0]
        vehicle_type = parts[1].lower()
        try:
            hours = float(parts[2])
        except:
            print("hours_parked phải là số.")
            continue

        # rules
        if hours <= 0:
            # must ignore invalid hours using continue
            print("Bỏ qua: hours_parked <= 0")
            continue
        if vehicle_type not in VALID_TYPES:
            print("Bỏ qua: loại xe không hợp lệ")
            continue

        fee = calc_fee(vehicle_type, hours)
        fees[vehicle_id] = fee
        total_revenue += fee
        count_by_type[vehicle_type] += 1

    print("\nKết quả phí theo xe (dict):")
    print(fees)
    print("\nTotal revenue:", total_revenue)
    print("Vehicle count:", count_by_type)
# Q2 – Parking Slot Management 
def question_2():
    print("\nQ2 – Parking Slot Management")
    capacity = safe_int_input("Nhập sức chứa bãi (capacity): ")
    if capacity < 0:
        print("capacity không hợp lệ.")
        return

    print("\nNhập sự kiện theo dòng: IN vehicle_id  hoặc  OUT vehicle_id")
    print("Ví dụ: IN A01")
    print("Gõ STOP để kết thúc.\n")

    parked = set()

    while True:
        line = input("Nhập sự kiện (hoặc STOP): ").strip()
        if line.upper() == "STOP":
            print("STOP → Dừng xử lý sự kiện.")
            break

        parts = line.split()
        if len(parts) != 2:
            print("Sai cú pháp. Ví dụ đúng: IN A01")
            continue

        event_type = parts[0].upper()
        vehicle_id = parts[1]

        if event_type == "IN":
            if len(parked) >= capacity:
                print(f"IN {vehicle_id} → Parking full")
            else:
                parked.add(vehicle_id)
                available = capacity - len(parked)
                print(f"IN {vehicle_id} → Parked: {parked}, Available slots: {available}")

        elif event_type == "OUT":
            if vehicle_id in parked:
                parked.remove(vehicle_id)
                available = capacity - len(parked)
                print(f"OUT {vehicle_id} → Parked: {parked}, Available slots: {available}")
            else:
                print(f"OUT {vehicle_id} → Vehicle not found, ignored")
        else:
            print("event_type chỉ được IN hoặc OUT.")
# Q3 – Parking Violation Detection 
def question_3():
    print("\n===== Q3 – Parking Violation Detection =====")
    print("Nhập record theo dòng: vehicle_id vehicle_type hours_parked amount_paid")
    print("Ví dụ: A01 car 5 30000")
    print("Gõ STOP để kết thúc.\n")

    records = {}

    while True:
        line = input("Nhập record (hoặc STOP): ").strip()
        if line.upper() == "STOP":
            break

        parts = line.split()
        if len(parts) != 4:
            print("Sai cú pháp. Ví dụ đúng: A01 car 5 30000")
            continue

        vehicle_id = parts[0]
        vehicle_type = parts[1].lower()

        try:
            hours = float(parts[2])
            paid = float(parts[3])
        except:
            print("hours_parked và amount_paid phải là số.")
            continue

        records[vehicle_id] = (vehicle_type, hours, paid)

    violations = {}
    total_unpaid = 0

    for vehicle_id, (v_type, hours, paid) in records.items():
        if v_type not in VALID_TYPES:
            violations[vehicle_id] = "Invalid vehicle type"
            continue

        if hours > 24:
            violations[vehicle_id] = "Exceeded maximum parking duration"
            continue

        if hours <= 0:
            violations[vehicle_id] = "Invalid parking hours"
            continue

        required_fee = calc_fee(v_type, hours)

        if paid < required_fee:
            violations[vehicle_id] = "Underpaid parking fee"
            total_unpaid += (required_fee - paid)

    print("\nViolations (dict):")
    print(violations)
    print("\nTotal unpaid amount:", int(round(total_unpaid)))
# Q4 – Smart Parking Statistics 
def question_4():
    print("\n===== Q4 – Smart Parking Statistics =====")
    print("Nhập dữ liệu theo dòng: vehicle_id vehicle_type hour_in hour_out")
    print("Ví dụ: A01 car 8 12")
    print("Gõ STOP để kết thúc.\n")

    data = []

    while True:
        line = input("Nhập record (hoặc STOP): ").strip()
        if line.upper() == "STOP":
            break

        parts = line.split()
        if len(parts) != 4:
            print("Sai cú pháp. Ví dụ đúng: A01 car 8 12")
            continue

        vehicle_id = parts[0]
        v_type = parts[1].lower()

        try:
            hour_in = float(parts[2])
            hour_out = float(parts[3])
        except:
            print("hour_in và hour_out phải là số.")
            continue

        data.append((vehicle_id, v_type, hour_in, hour_out))

    total_duration_by_type = {"bike": 0.0, "car": 0.0, "truck": 0.0}
    count_by_type = {"bike": 0, "car": 0, "truck": 0}
    unique_vehicles = set()

    longest_vehicle_id = None
    longest_duration = -1

    for vehicle_id, v_type, hour_in, hour_out in data:
        if v_type not in VALID_TYPES:
            continue
        if hour_out < hour_in:
            # rule: skip invalid
            continue

        duration = hour_out - hour_in
        total_duration_by_type[v_type] += duration
        count_by_type[v_type] += 1
        unique_vehicles.add(vehicle_id)

        if duration > longest_duration:
            longest_duration = duration
            longest_vehicle_id = vehicle_id

    print("\nAverage duration:")
    for v_type in ["bike", "car", "truck"]:
        if count_by_type[v_type] == 0:
            continue
        avg = total_duration_by_type[v_type] / count_by_type[v_type]
        print(f"{v_type}: {avg:.1f} hours")

    if longest_vehicle_id is None:
        print("\nLongest parking vehicle: N/A")
    else:
        print(f"\nLongest parking vehicle: {longest_vehicle_id} ({longest_duration:.1f} hours)")

    print("Unique vehicles:", len(unique_vehicles))
# Q5 – Full Parking System 
def question_5():
    print("\n===== Q5 – Full Parking System (Capstone) =====")
    print(f"Sức chứa tối đa: {MAX_CAPACITY_Q5}")
    print("Loại xe hỗ trợ: bike, car, truck")
    print("Phụ phí giờ cao điểm: +20% (7–9, 17–19)\n")

    parked = {}   # vehicle_id -> {"type": str, "hour_in": float}
    history = []  # checkout history
    total_revenue = 0

    def menu_q5():
        print("\n----- Q5 MENU -----")
        print("1. Thủ tục nhận xe")
        print("2. Thủ tục trả xe")
        print("3. Hiển thị trạng thái đỗ xe")
        print("4. Hiển thị báo cáo doanh thu")
        print("0. Hệ thống thoát hiếm")
        print("-------------------")

    while True:
        menu_q5()
        choice = input("Chọn: ").strip()

        if choice == "1":
            if len(parked) >= MAX_CAPACITY_Q5:
                print("Từ chối làm thủ tục nhận phòng: Bãi đỗ xe đã đầy.")
                continue

            vehicle_id = input("Nhập mã_id_xe: ").strip()
            vehicle_type = input("Nhập loại_xe (bike/car/truck): ").strip().lower()
            hour_in = safe_float_input("Nhập giờ vào (0–24): ")

            if vehicle_type not in VALID_TYPES:
                print("Từ chối làm thủ tục nhận phòng: loại xe không hợp lệ.")
                continue
            if vehicle_id in parked:
                print("Từ chối làm thủ tục nhận phòng: xe đã đỗ.")
                continue
            if not (0 <= hour_in <= 24):
                print("Từ chối làm thủ tục nhận phòng: giờ_vào không nằm trong khoảng 0–24.")
                continue

            parked[vehicle_id] = {"type": vehicle_type, "hour_in": hour_in}
            print(f"Vehicle {vehicle_id} parked successfully.")

        elif choice == "2":
            vehicle_id = input("Nhập mã_id_xe: ").strip()
            hour_out = safe_float_input("Nhập giờ ra (0–24): ")

            if vehicle_id not in parked:
                print("Từ chối thanh toán: Không tìm thấy xe.")
                continue
            if not (0 <= hour_out <= 24):
                print("Từ chối thanh toán: giờ ra không hợp lệ (0–24).")
                continue

            hour_in = parked[vehicle_id]["hour_in"]
            v_type = parked[vehicle_id]["type"]

            if hour_out <= hour_in:
                print("Từ chối thanh toán: giờ ra ≤ giờ vào.")
                continue

            duration = hour_out - hour_in
            fee = calc_fee(v_type, duration, hour_in=hour_in)

            total_revenue += fee
            history.append({
                "id": vehicle_id,
                "type": v_type,
                "hour_in": hour_in,
                "hour_out": hour_out,
                "duration": duration,
                "fee": fee
            })
            del parked[vehicle_id]

            print(f"Parking fee: {fee} VND")

        elif choice == "3":
            print(f"\nVehicles currently parked: {len(parked)}")
            if len(parked) > 0:
                for vid, info in parked.items():
                    print(f"{vid} ({info['type']}), entered at {info['hour_in']}")
            print(f"Available slots: {MAX_CAPACITY_Q5 - len(parked)}")

        elif choice == "4":
            count_by_type = {"bike": 0, "car": 0, "truck": 0}
            longest_id = None
            longest_duration = -1

            for item in history:
                count_by_type[item["type"]] += 1
                if item["duration"] > longest_duration:
                    longest_duration = item["duration"]
                    longest_id = item["id"]

            print("\n----- REVENUE REPORT -----")
            print("Total revenue:", total_revenue)
            print("Vehicles by type:")
            print("bike:", count_by_type["bike"])
            print("car:", count_by_type["car"])
            print("truck:", count_by_type["truck"])

            if longest_id is None:
                print("Longest parked vehicle: N/A")
            else:
                print(f"Longest parked vehicle: {longest_id} ({longest_duration:.1f} hours)")
            print("--------------------------")

        elif choice == "0":
            print("\n===== FINAL SUMMARY REPORT =====")
            print("Total revenue:", total_revenue)

            count_by_type = {"bike": 0, "car": 0, "truck": 0}
            longest_id = None
            longest_duration = -1

            for item in history:
                count_by_type[item["type"]] += 1
                if item["duration"] > longest_duration:
                    longest_duration = item["duration"]
                    longest_id = item["id"]

            print("Vehicles completed checkout by type:", count_by_type)
            if longest_id is None:
                print("Longest parked vehicle: N/A")
            else:
                print(f"Longest parked vehicle: {longest_id} ({longest_duration:.1f} hours)")

            print("Chương trình kết thúc. Không chấp nhận thêm thông tin nào nữa.")
            break

        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
# MAIN MENU
def main():
    while True:
        print("\n===== PARKING ASSIGNMENT MENU =====")
        print("1. Q1 – Parking Fee Calculator")
        print("2. Q2 – Parking Slot Management")
        print("3. Q3 – Parking Violation Detection")
        print("4. Q4 – Smart Parking Statistics")
        print("5. Q5 – Full Parking System")
        print("0. Exit")
        print("==================================")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            question_1()
        elif choice == "2":
            question_2()
        elif choice == "3":
            question_3()
        elif choice == "4":
            question_4()
        elif choice == "5":
            question_5()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


# ---------- RUN PROGRAM ----------
main()
