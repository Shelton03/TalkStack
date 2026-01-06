import re

# Current regex
WHATSAPP_CHAT_REGEX = re.compile(
    r"\[(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}(:\d{2})?( [AP]M)?)\] ([^:]+): (.*)",
    re.IGNORECASE
)

# Test line (exact copy from logs)
test_line = "[11/19/25, 6:41:43 PM] Sa-fe-Spa-ciooo⭐️: ‎Messages and calls are end-to-end encrypted."

print("Testing current regex:")
print(f"Line: {test_line}")
print(f"Line bytes: {test_line.encode('utf-8')}")
print()

match = WHATSAPP_CHAT_REGEX.match(test_line)
if match:
    print("✅ MATCHED!")
    print(f"Groups: {match.groups()}")
else:
    print("❌ NO MATCH")
    
    # Test each part
    print("\nTesting components:")
    
    # Test bracket and date
    if re.match(r"\[\d{1,2}/\d{1,2}/\d{2,4}", test_line):
        print("  ✅ Opening bracket and date OK")
    else:
        print("  ❌ Opening bracket or date failed")
    
    # Test time with seconds
    if re.search(r"\d{1,2}:\d{2}:\d{2}", test_line):
        print("  ✅ Time with seconds OK")
    else:
        print("  ❌ Time with seconds failed")
    
    # Test AM/PM
    if re.search(r" [AP]M", test_line):
        print("  ✅ AM/PM OK")
    else:
        print("  ❌ AM/PM failed")
    
    # Test closing bracket
    if "] " in test_line:
        print("  ✅ Closing bracket with space OK")
    else:
        print("  ❌ Closing bracket with space failed")
    
    # Test sender and colon
    sender_match = re.search(r"\] ([^:]+):", test_line)
    if sender_match:
        print(f"  ✅ Sender found: '{sender_match.group(1)}'")
    else:
        print("  ❌ Sender pattern failed")

print("\n" + "="*60)
print("Testing simpler regex:")
simple_regex = re.compile(r"\[([^\]]+)\] ([^:]+): (.*)")
match2 = simple_regex.match(test_line)
if match2:
    print("✅ Simple regex MATCHED!")
    print(f"Timestamp: {match2.group(1)}")
    print(f"Sender: {match2.group(2)}")
    print(f"Message: {match2.group(3)}")
else:
    print("❌ Simple regex failed too")
