import yaml
import json

# Đọc file YAML
with open('openAPI.yaml', 'r', encoding='utf-8') as file:
    yaml_data = yaml.safe_load(file)

# Chuyển đổi sang JSON và lưu vào file
with open('openAPI.json', 'w', encoding='utf-8') as file:
    json.dump(yaml_data, file, ensure_ascii=False, indent=2)

print("Chuyển đổi thành công từ YAML sang JSON!") 