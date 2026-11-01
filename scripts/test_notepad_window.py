from pywinauto import Application
import time
#Launch Notepad


def test_notepad_window():
    # Launch Notepad++
    app = Application(backend="uia").start(r"C:\Program Files\Notepad++\notepad++.exe")

    # Identify Notepad++ window
    main = app.window(title_re=".*Notepad.*")

    # Wait until visible
    main.wait("visible", timeout=20)

    # Enter text
    main.type_keys("Welcome to Pywinauto Automation!")

    def checking_window():
        time.sleep(2)
        main.child_window(title="Generate...", control_type="MenuItem").click_input()
        time.sleep(2)
        gen_MDS_dig = main.child_window(title="Generate MD5 digest", control_type="Window")
        gen_MDS_dig.child_window(title="Treat each line as a separate string", control_type="CheckBox").toggle()
        time.sleep(2)
        gen_MDS_dig.child_window(title="Close", control_type="Button", found_index=0).click_input()
        time.sleep(2)

    # Navigate File -> Save As -> identify menus using menu_select
    main.menu_select("Tools->MD5")
    print(main.print_control_identifiers())  # to print all the controls in the window
    checking_window()

    # identify the menu items using child_window and click on them
    main.child_window(title="Tools", control_type="MenuItem").click_input()
    time.sleep(2)
    main.child_window(title="MD5", control_type="MenuItem").click_input()
    time.sleep(2)
    checking_window()
    main.close()















