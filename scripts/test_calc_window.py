from pywinauto import Application
import time


def test_verify_window():
    # verify Scientific Calculator window
    app = Application(backend="uia").start("calc.exe")
    # Wait for Calculator to launch
    app.connect(title_re=".*Calculator.*", timeout=10)
    calc = app.top_window()
    calc.child_window(title="Open Navigation", control_type="Button").click_input()
    time.sleep(1)
    print(calc.print_control_identifiers())
    calc.child_window(auto_id="Scientific", control_type="ListItem").click_input()
    calc.child_window(title="Two", control_type="Button").click_input()
    calc.child_window(title="Three", control_type="Button").click_input()
    calc.child_window(auto_id="expButton", control_type="Button").click_input()
    time.sleep(2)
    # print(calc.print_control_identifiers())
    calc.child_window(title="Five", control_type="Button").click_input()
    calc.child_window(auto_id="equalButton", control_type="Button").click_input()
    result = calc.child_window(auto_id="CalculatorResults", control_type="Text").window_text()
    time.sleep(2)
    print("result->", result)
    amount = result.split(" ")[2]
    print("amount->", amount)

    # verify Currency Calculator window
    calc.child_window(title="Open Navigation", control_type="Button").click_input()
    time.sleep(1)
    calc.child_window(auto_id="Currency", control_type="ListItem").click_input()
    calc.child_window(title="Two", control_type="Button").click_input()
    calc.child_window(title="Three", control_type="Button").click_input()
    print(calc.print_control_identifiers())
    time.sleep(2)
    val1_from = calc.child_window(title_re=".*Convert from.*", control_type="Text", auto_id='Value1')
    val1_text = val1_from.window_text()
    val1_from.draw_outline(colour="green", thickness=3)
    print("val1_text - ", val1_text)
    time.sleep(4)
    val2_to = calc.child_window(title_re=".*Converts into .*", control_type="Text", auto_id='Value2')
    val2_text = val2_to.window_text()
    val2_to.draw_outline(colour="red", thickness=4)
    print("val2_text - ", val2_text)
    time.sleep(5)
    calc.close()
    time.sleep(1)