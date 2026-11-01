from pywinauto import Desktop
import time
from pathlib import Path
from pywinauto import Application, mouse
import random
from pywinauto.keyboard import send_keys

def test_windows_automation():
    LOGIN_WINDOW = "Login"
    REGI_WINDOW = "Registration Page - Automation Practice"
    # 1. Launch the app (start() does not block, unlike subprocess.run)
    file_path = Path(__file__).resolve().parents[1] / "application/CourseRegistration.exe"
    print("file_path->", file_path)
    app = Application(backend="uia").start(str(file_path))
    # 2. identify the login window
    login = app.window(title=LOGIN_WINDOW)
    # wait for the login window to be ready
    login.wait("visible ready", timeout=15)
    # 3. Enter username and password
    un = login.child_window(auto_id="username", control_type="Edit")
    un.set_edit_text("admin")
    # highlight the username field for visual confirmation
    un.draw_outline(colour="red", thickness=3)
    # get and print the value, visibility, and enabled state of the username field
    print("UN Value -> ", un.get_value())
    print("UN is_visible -> ", un.is_visible())
    print("UN is_enabled -> ", un.is_enabled())
    login.child_window(auto_id="password", control_type="Edit").set_edit_text("admin")
    login.child_window(auto_id="loginBtn", control_type="Button").click_input()
    time.sleep(4)
    Reg_Win = app.window(title=REGI_WINDOW)
    Reg_Win.wait("visible ready", timeout=15)
    print("Logged in:", Reg_Win.exists())
    Reg_Win.maximize()
    time.sleep(5)
    first_name_val = f"Nagaraju Gandlur {random.random()} "
    Reg_Win.child_window(auto_id="fullName", control_type="Edit").set_edit_text(first_name_val)
    first_name = Reg_Win.child_window(auto_id="firstName", control_type="Edit")
    first_name.set_edit_text(first_name_val)
    country_select = Reg_Win.child_window(auto_id="countrySelect", control_type="ComboBox")
    country_select.click_input()
    time.sleep(2)
    country_select.child_window(title="India", control_type="ListItem").click_input()
    country_select.click_input()
    country_select.descendants(control_type="ListItem")[1].click_input()

    ### drag and drop
    radiobutton = Reg_Win.child_window(auto_id="postGraduation", control_type="RadioButton")
    radiobutton.set_focus()

    drag_source = Reg_Win.child_window(auto_id="dragSource", control_type="Text").wrapper_object()
    drag_source.set_focus()
    print("drag_source->", drag_source)
    drop_source = Reg_Win.child_window(auto_id="dropZone", control_type="Text").wrapper_object()
    print("drop_source->", drop_source)
    # Get the center coordinates of both source and target elements
    src_point = drag_source.rectangle().mid_point()
    print("src_point-> mid_point", src_point)
    dst_point = drop_source.rectangle().mid_point()
    print("dst_point-> mid_point", dst_point)

    # Perform the drag and drop using the global mouse module with exact screen coordinates
    mouse.press(button='left', coords=(src_point.x, src_point.y))
    mouse.move(coords=(dst_point.x, dst_point.y))
    mouse.release(button='left', coords=(dst_point.x, dst_point.y))

    # Handling checkboxes and radio buttons
    check_box = Reg_Win.child_window(auto_id="female", control_type="CheckBox")
    is_checked = check_box.get_toggle_state()  # 1 is checked, 0 is unchecked
    print(f"Is checked: {is_checked}")
    check_box.toggle()
    radiobutton = Reg_Win.child_window(auto_id="postGraduation", control_type="RadioButton")
    radiobutton.set_focus()
    radiobutton_selected = radiobutton.is_selected()  # 1 is checked, 0 is unchecked
    print(f"Is radiobutton_selected: {radiobutton_selected}")
    radiobutton.select()
    time.sleep(8)

    # Handling Tables
    table = Reg_Win.child_window(auto_id="courseTable", control_type="Table")
    table.set_focus()
    data_4 = table.child_window(control_type="DataItem", title="Joining Row 4")
    data_4.set_focus()
    data_4.click_input()
    data_4.double_click_input()
    dropdown = table.child_window(title="Yes", control_type="ListItem")
    dropdown.click_input()

    # data_4_link = table.child_window(control_type="DataItem",title="Link Row 4")
    # data_4_link.click_input()

    ### file upload
    file_button = Reg_Win.child_window(auto_id="fileUploadBtn", control_type="Button")
    file_button.set_focus()
    file_button.click_input()
    time.sleep(5)  # title="File name: control_type="Edit"
    file_path = "C:\\Users\\naga1\\OneDrive\\Desktop\\ALL\\Cricket.xlsx"
    Reg_Win.child_window(title="File name:", control_type="Edit").set_edit_text(file_path)
    Reg_Win.child_window(title="Cancel", control_type="Button").click_input()
    time.sleep(5)

    # Handling Dropdowns and  Get the text from dropdown items
    district_dp = Reg_Win.child_window(auto_id="district", control_type="ComboBox")
    district_dp.click_input()
    time.sleep(1)
    items = district_dp.descendants(control_type="ListItem")

    for index, item in enumerate(items):
        print(index, item.window_text())

    District = "Yadgir"
    send_keys(District)
    time.sleep(0.5)
    Reg_Win.child_window(title=District, control_type="ListItem").click_input()
    time.sleep(2)
    Reg_Win.child_window(auto_id="openNewWindowBtn", control_type="Button").click_input()
    time.sleep(2)
    Reg_Win.child_window(auto_id="mainPerson", control_type="Edit").set_edit_text(District + "MainPerson")
    Reg_Win.child_window(auto_id="talukSelect", control_type="ComboBox").click_input()
    time.sleep(1)
    Reg_Win.child_window(title=District, control_type="ListItem").click_input()
    district_window = Reg_Win.child_window(title=District, control_type="Window")
    district_window.close()
    time.sleep(1)

    # alerts
    Reg_Win.child_window(title="DD-MM-YYYY", control_type="Edit").set_focus()
    new_window = Reg_Win.child_window(auto_id="showAlertBtn", control_type="Button")
    new_window.set_focus()
    Reg_Win.child_window(title="Show Prompt", control_type="Button").click_input()
    Reg_Win.child_window(auto_id="promptInput", control_type="Edit").set_edit_text("NAGARAJU")
    Reg_Win.child_window(auto_id="promptOk", control_type="Button").click_input()
    time.sleep(2)

    # double click
    dbl_ck = Reg_Win.child_window(auto_id="doubleClickBtn", control_type="Text")
    dbl_ck.double_click_input()

    # Selecting multiple items in a listbox using shift key
    dropdown = Reg_Win.child_window(auto_id="hobbies", control_type="List")
    dropdown.set_focus()
    dropdown.get_item("Sports").click_input(pressed="shift")
    dropdown.get_item("Music").click_input(pressed="shift")
    dropdown.get_item("Travel").click_input(pressed="shift")

    disabled_object = Reg_Win.child_window(auto_id="disabledField", control_type="Edit")
    if disabled_object.is_enabled():
        print("Disabled")
    else:
        print("Enabled")

    # right click
    rc = Reg_Win.child_window(auto_id="rightclick", control_type="Text")
    rc.set_focus()
    rc.right_click_input()  # rc.click_input(button='right')
    time.sleep(2)
    Reg_Win.child_window(title="Share", control_type="MenuItem").click_input()
    time.sleep(2)
    Reg_Win.child_window(title="OK", control_type="Button").click_input()
    time.sleep(2)

    # Save and Download
    save_button = Reg_Win.child_window(title="Save", control_type="Button")
    save_button.set_focus()
    save_button.click_input()
    time.sleep(5)
    OK_ed = Reg_Win.child_window(title="OK", control_type="Button")
    OK_ed.set_focus()
    OK_ed.click_input()
    time.sleep(5)
    # Download XLSX
    download_file = "xl"
    if download_file == "xl":
        button_name = "Download XLSX"
    else:
        button_name = "Download TXT"
    dwn_file_type = Reg_Win.child_window(title=button_name, control_type="Button")
    dwn_file_type.set_focus()
    dwn_file_type.draw_outline(colour="red", thickness=3)
    dwn_file_type.click_input()
    Reg_Win.child_window(title="Cancel", control_type="Button").click_input()
    time.sleep(5)
    Reg_Win.close()