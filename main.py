from abc import ABC, abstractmethod

class Champion(ABC):

    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int):
        self.champion_id = champion_id
        self.name = name
        self.base_hp = base_hp if base_hp > 0 else 100
        self.base_atk = base_atk if base_atk > 0 else 100

    @abstractmethod
    def calculate_skill_damage(self) -> float:
        pass

    def get_combat_power(self) -> float:
        return self.base_hp + self.calculate_skill_damage() * 1.5

    def __add__(self, other):
        if isinstance(other, Champion):
            return self.get_combat_power() + other.get_combat_power()
        elif isinstance(other, (int, float)):
            return self.get_combat_power() + other
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, (int, float)):
            return self.get_combat_power() + other
        return NotImplemented

    def __gt__(self, other) -> bool:
        if isinstance(other, Champion):
            return self.get_combat_power() > other.get_combat_power()
        return NotImplemented


class Warrior(Champion):

    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int, shield_bonus: int):
        super().__init__(champion_id, name, base_hp, base_atk)
        self.shield_bonus = shield_bonus

    def calculate_skill_damage(self) -> float:
        return self.base_atk * 2 + self.shield_bonus


class Mage(Champion):

    def __init__(self, champion_id: str, name: str, base_hp: int, base_atk: int, ability_power: float):
        super().__init__(champion_id, name, base_hp, base_atk)
        self.ability_power = ability_power

    def calculate_skill_damage(self) -> float:
        return self.base_atk * self.ability_power


def get_class_name(champion: Champion) -> str:
    return type(champion).__name__


def get_unique_stat(champion: Champion) -> str:
    if isinstance(champion, Warrior):
        return f"Armor: {champion.shield_bonus}"
    elif isinstance(champion, Mage):
        return f"Mana: {int(champion.ability_power * 100)}"
    return "N/A"


def find_champion(pool: list, champion_id: str):
    for c in pool:
        if c.champion_id == champion_id:
            return c
    return None


def display_pool(pool: list):
    print("\n--- DANH SÁCH QUÂN CỜ TRONG BỂ TƯỚNG ---")
    if not pool:
        print("Bể tướng hiện đang trống.")
        return

    header = f"{'Mã':<7}| {'Tên tướng':<22}| {'Hệ':<10}| {'HP':<7}| {'ATK':<7}| {'Chỉ số riêng':<20}| Chiến lực"
    print(header)
    print("-" * 101)
    for c in pool:
        print(
            f"{c.champion_id:<7}| {c.name:<22}| {get_class_name(c):<10}| "
            f"{c.base_hp:<7}| {c.base_atk:<7}| {get_unique_stat(c):<20}| {int(c.get_combat_power())}"
        )
    print("-" * 101)


def add_champion(pool: list):
    print("\n--- THÊM QUÂN CỜ MỚI ---")
    print("Chọn hệ tướng:")
    print("1. Warrior (Chiến binh)")
    print("2. Mage (Pháp sư)")

    choice = input("Lựa chọn của bạn (1/2): ").strip()
    if choice not in ("1", "2"):
        print("Lựa chọn không hợp lệ.")
        return

    class_name = "WARRIOR" if choice == "1" else "MAGE"
    print(f"\n--- TẠO TƯỚNG {class_name} ---")

    champion_id = input("Nhập mã tướng: ").strip().upper()
    if find_champion(pool, champion_id):
        print(f"Lỗi: Mã tướng '{champion_id}' đã tồn tại trong bể tướng!")
        return

    name = input("Nhập tên tướng: ").strip()

    try:
        base_hp = int(input("Nhập HP: "))
        base_atk = int(input("Nhập ATK: "))
    except ValueError:
        print("HP và ATK phải là số nguyên. Thêm tướng thất bại.")
        return
    if base_hp <= 0:
        print("HP <= 0, tự động đặt về 100.")
    if base_atk <= 0:
        print("ATK <= 0, tự động đặt về 100.")

    if choice == "1":
        try:
            shield_bonus = int(input("Nhập Armor: "))
        except ValueError:
            print("Armor phải là số nguyên. Thêm tướng thất bại.")
            return
        new_champion = Warrior(champion_id, name, base_hp, base_atk, shield_bonus)
    else:
        try:
            ability_power = float(input("Nhập Ability Power (ví dụ: 1.5): "))
        except ValueError:
            print("Ability Power phải là số thực. Thêm tướng thất bại.")
            return
        new_champion = Mage(champion_id, name, base_hp, base_atk, ability_power)

    pool.append(new_champion)
    print(f"\nThêm tướng {class_name} thành công!")
    print(f"Mã: {new_champion.champion_id} | Tên: {new_champion.name} | Chiến lực: {int(new_champion.get_combat_power())}")


def compare_champions(pool: list):
    print("\n--- SO SÁNH SỨC MẠNH 2 QUÂN CỜ ---")
    id1 = input("Nhập mã tướng thứ nhất: ").strip().upper()
    id2 = input("Nhập mã tướng thứ hai: ").strip().upper()

    c1 = find_champion(pool, id1)
    c2 = find_champion(pool, id2)

    if not c1:
        print(f"Mã tướng [{id1}] không hợp lệ, bỏ qua!")
        return
    if not c2:
        print(f"Mã tướng [{id2}] không hợp lệ, bỏ qua!")
        return

    print("\nThông tin so sánh:")
    print(f"{c1.champion_id} - {c1.name:<20} | Hệ: {get_class_name(c1):<8} | Chiến lực: {int(c1.get_combat_power())}")
    print(f"{c2.champion_id} - {c2.name:<20} | Hệ: {get_class_name(c2):<8} | Chiến lực: {int(c2.get_combat_power())}")

    if c1 > c2:
        print(f"Kết quả: {c1.champion_id} - {c1.name} mạnh hơn {c2.champion_id} - {c2.name}.")
    elif c2 > c1:
        print(f"Kết quả: {c2.champion_id} - {c2.name} mạnh hơn {c1.champion_id} - {c1.name}.")
    else:
        print("Kết quả: Hai tướng có chiến lực bằng nhau!")


def calculate_team_power(pool: list):
    print("\n--- TÍNH TỔNG CHIẾN LỰC ĐỘI HÌNH RA SÂN ---")
    raw = input("Nhập danh sách mã tướng, cách nhau bằng dấu phẩy: ")
    ids = [x.strip().upper() for x in raw.split(",")]

    team = []
    for cid in ids:
        c = find_champion(pool, cid)
        if c:
            team.append(c)
        else:
            print(f"Mã tướng [{cid}] không hợp lệ, bỏ qua!")

    if not team:
        print("Không có tướng hợp lệ nào trong đội hình.")
        return

    print("\nDanh sách đội hình:")
    total = 0
    for i, c in enumerate(team, 1):
        print(f"{i}. {c.champion_id} - {c.name:<20} | Chiến lực: {int(c.get_combat_power())}")
        total = total + c

    print(f"Tổng chiến lực đội hình: {int(total)}")


def main():

    champion_pool = [
        Warrior("WAR01", "Rikkei Knight", 1200, 300, 150),
        Warrior("WAR02", "Steel Guardian", 1500, 250, 200),
        Mage("MAG01", "Rikkei Wizard", 800, 500, 2.5),
    ]

    print("=" * 50)
    print("  RIKKEI RPG - AUTO-BATTLER MANAGER")
    print("=" * 50)

    running = True
    while running:
        print("\n--- MENU CHÍNH ---")
        print("1. Hiển thị bể tướng")
        print("2. Thêm quân cờ mới")
        print("3. So sánh 2 quân cờ")
        print("4. Tính tổng chiến lực đội hình")
        print("5. Thoát")

        choice = input("Chọn chức năng (1-5): ").strip()

        if choice == "1":
            display_pool(champion_pool)
        elif choice == "2":
            add_champion(champion_pool)
        elif choice == "3":
            compare_champions(champion_pool)
        elif choice == "4":
            calculate_team_power(champion_pool)
        elif choice == "5":
            print("Cảm ơn bạn đã sử dụng Rikkei RPG - Auto-Battler Manager!")
            running = False
        else:
            print("Lựa chọn không hợp lệ, vui lòng nhập từ 1 đến 5.")


if __name__ == "__main__":
    main()