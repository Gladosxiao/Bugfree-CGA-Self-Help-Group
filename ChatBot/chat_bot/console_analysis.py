def console_analysis(test_group, content):
    test_group.send(content)
    exec(content)
