# -*- coding: utf-8 -*-
import MySQLdb as mdb 
import sys
try:
    conn = mdb.connect(host='localhost',user='root', 
        passwd='liuhai159357', db='forest')
    cursor = conn.cursor()
    result = cursor.execute("SELECT TITLE,DOC,DICTID,LY,FBR FROM vweb_news_list")
    while (result):
        title = cursor.fetchone()[0]
        zhongwen = cursor.fetchone()[1]
        dictid = cursor.fetchone()[2]
        ly = cursor.fetchone()[3]
        fbr = cursor.fetchone()[4]

        author
        print zhongwen


    cursor.close()
    conn.close()

except IOError, e:
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)



# INSERT INTO `vweb_news_list` VALUES (
#     '20111216161100109',
#     '湖北省森林公安局局长陈毓安到洪湖检查调研森林公安和森林防火工作',
#     '20111216161100109.html',
#     '0',
#     '20111108164603515',
#     0x3C5020636C6173733D4D736F4E6F726D616C207374796C653D224D415247494E3A2030636D2030636D203070743B204C494E452D4845494748543A20323870743B20544558542D414C49474E3A2063656E7465723B206D736F2D6C696E652D6865696768742D72756C653A2065786163746C792220616C69676E3D63656E7465723E3C5350414E207374796C653D22464F4E542D53495A453A20313870743B20464F4E542D46414D494C593A20B7BDD5FDD0A1B1EACBCEBCF2CCE5223EBAFEB1B1CAA1C9ADC1D6B9ABB0B2BED6BED6B3A4B3C2D8B9B0B23C5350414E206C616E673D454E2D55533E3C3F786D6C3A6E616D65737061636520707265666978203D206F206E73203D202275726E3A736368656D61732D6D6963726F736F66742D636F6D3A6F66666963653A6F666669636522202F3E3C6F3A703E3C2F6F3A703E3C2F5350414E3E3C2F5350414E3E3C2F503E0D0A3C5020636C6173733D4D736F4E6F726D616C207374796C653D224D415247494E3A2030636D2030636D203070743B204C494E452D4845494748543A20323870743B20544558542D414C49474E3A2063656E7465723B206D736F2D6C696E652D6865696768742D72756C653A2065786163746C792220616C69676E3D63656E7465723E3C5350414E207374796C653D22464F4E542D53495A453A20313870743B20464F4E542D46414D494C593A20B7BDD5FDD0A1B1EACBCEBCF2CCE5223EB5BDBAE9BAFEBCECB2E9B5F7D1D0C9ADC1D6B9ABB0B2BACDC9ADC1D6B7C0BBF0B9A4D7F73C5350414E206C616E673D454E2D55533E3C6F3A703E3C2F6F3A703E3C2F5350414E3E3C2F5350414E3E3C2F503E0D0A3C5020636C6173733D4D736F4E6F726D616C207374796C653D224D415247494E3A2030636D2030636D203070743B204C494E452D4845494748543A20323870743B20544558542D414C49474E3A2063656E7465723B206D736F2D6C696E652D6865696768742D72756C653A2065786163746C792220616C69676E3D63656E7465723E3C5350414E206C616E673D454E2D5553207374796C653D22464F4E542D53495A453A203970743B20464F4E542D46414D494C593A20B7C2CBCE5F474232333132223E3C6F3A703E266E6273703B3C2F6F3A703E3C2F5350414E3E3C2F503E0D0A3C5020636C6173733D4D736F4E6F726D616C207374796C653D224D415247494E3A2030636D2030636D203070743B20544558542D494E44454E543A20333270743B204C494E452D4845494748543A20323870743B206D736F2D6C696E652D6865696768742D72756C653A2065786163746C793B206D736F2D636861722D696E64656E742D636F756E743A20322E30223E3C3F786D6C3A6E616D65737061636520707265666978203D20737431206E73203D202275726E3A736368656D61732D6D6963726F736F66742D636F6D3A6F66666963653A736D6172747461677322202F3E3C7374313A6368736461746520773A73743D226F6E22204973524F43446174653D2246616C7365222049734C756E6172446174653D2246616C736522204461793D223922204D6F6E74683D2231312220596561723D2232303131223E3C5350414E206C616E673D454E2D5553207374796C653D22464F4E542D53495A453A20313670743B20464F4E542D46414D494C593A20B7C2CBCE5F474232333132223E323031313C2F5350414E3E3C5350414E207374796C653D22464F4E542D53495A453A20313670743B20464F4E542D46414D494C593A20B7C2CBCE5F474232333132223EC4EA3C5350414E206C616E673D454E2D55533E31313C2F5350414E3ED4C23C5350414E206C616E673D454E2D55533E393C2F5350414E3EC8D53C2F5350414E3E3C2F7374313A636873646174653E3C5350414E207374796C653D22464F4E542D53495A453A20313670743B20464F4E542D46414D494C593A20B7C2CBCE5F474232333132223EA3ACCAA1C9ADC1D6B9ABB0B2BED6BED6B3A4B3C2D8B9B0B2D4DABEA3D6DDCAD0C9ADC1D6B9ABB0B2BED6BED6B3A4C0EEBBAAD0DBA1A2BAE9BAFECAD0C1D6D2B5BED6BED6B3A4B6C5D2ABC6BDA1A2BAE9BAFECAD0C9ADC1D6B9ABB0B2BED6BED6B3A4D0A4CCFACAABB5C4C5E3CDACCFC2BCECB2E9B5F7D1D0BAE9BAFEC9ADC1D6B9ABB0B2BCB0C9ADC1D6B7C0BBF0B9A4D7F7A1A33C5350414E206C616E673D454E2D55533E3C6F3A703E3C2F6F3A703E3C2F5350414E3E3C2F5350414E3E3C2F503E0D0A3C5020636C6173733D4D736F4E6F726D616C207374796C653D224D415247494E3A2030636D2030636D203070743B20544558542D494E44454E543A20333270743B204C494E452D4845494748543A20323870743B206D736F2D6C696E652D6865696768742D72756C653A2065786163746C793B206D736F2D636861722D696E64656E742D636F756E743A20322E30223E3C5350414E207374796C653D22464F4E542D53495A453A20313670743B20464F4E542D46414D494C593A20B7C2CBCE5F474232333132223ED4DAB5F7D1D0D6D0A3ACB3C2D8B9B0B2BED6B3A4D2BBD0D0CAD7CFC8BCECB2E9C1CBBAE9BAFECAAAB5D8D7D4C8BBB1A3BBA4C7F8B5C4BDA8C9E8C7E9BFF6A3ACB2A2B3CBB4ACD1D8BAFEB2ECBFB4C1CBCAAAB5D8B1A3BBA4C7F8B5C4B9DCC0EDCFD6D7B4A3ACB6D4BDF1C4EABAE9BAFEBAB5C7E9BAF3C6DAB9DCC0EDCCE1B3F6C1CBD6B8B5BCD0D4D2E2BCFBA1A3CBE6BAF3A3ACD6D8B5E3BCECB2E9C1CBBAE9BAFEC9ADC1D6B9ABB0B2BBF9B4A1C9E8CAA9BDA8C9E8BACDD6B5B0E0B1B8C7DAC7E9BFF6A1A2D1AFCECAC1CBD2B5CEF1D3C3B7BFBDA8C9E8BDF8D5B9C7E9BFF6A3ACB2A2D3EBD6B5B0E0C3F1BEAFBDBBD0C4CCB8D0C4A3ACC1CBBDE2C3F1BEAFB5C4B9A4D7F7A1A2D1A7CFB0A1A2C9FABBEEB5C8C7E9BFF6A1A3B3C2BED6B3A4D4DABCECB2E9C9ADC1D6B7C0BBF0D6B5B0E0CAB1A3ACB1DFBFB4D6B5B0E0BCC7C2BCB1DFB3C6D4DEBAE9BAFEB5C4B7C0BBF0D6B5B0E0B9A4D7F7D7F6B5C3BADCBAC3A3ACBADCB5BDCEBBA3ACD6B5B0E0C8CBD4B1BCE1CAD8B8DACEBBA3ACD6B5B0E0BCC7C2BCC8ABC3E6CFB8D6C2A3ACD6B5B5C3D1A7CFB0A3ACD6B5B5C3BDE8BCF8A1A33C5350414E206C616E673D454E2D55533E3C6F3A703E3C2F6F3A703E3C2F5350414E3E3C2F5350414E3E3C2F503E0D0A3C5020636C6173733D4D736F4E6F726D616C207374796C653D224D415247494E3A2030636D2030636D203070743B20544558542D494E44454E543A20333270743B204C494E452D4845494748543A20323870743B206D736F2D6C696E652D6865696768742D72756C653A2065786163746C793B206D736F2D636861722D696E64656E742D636F756E743A20322E30223E3C5350414E207374796C653D22464F4E542D53495A453A20313670743B20464F4E542D46414D494C593A20B7C2CBCE5F474232333132223ED4DABBE1D2E9CAD2BDF8D0D0D7F9CCB8CAB1A3ACB3C2D8B9B0B2BED6B3A4D4DAB7D6B1F0CCFDC8A1C1CBCAD0C1D6D2B5BED6BED6B3A4B6C5D2ABC6BDA1A2C9ADC1D6B9ABB0B2BED6BED6B3A4D0A4CCFACAABB5C4B9A4D7F7BBE3B1A8BAF3A3ACB6D43C2F5350414E3E3C5350414E207374796C653D22464F4E542D53495A453A20313670743B20434F4C4F523A20626C61636B3B20464F4E542D46414D494C593A20B7C2CBCE5F4742323331323B206D736F2D61736369692D666F6E742D66616D696C793A202754696D6573204E657720526F6D616E27223EBDFCC4EAC0B43C2F5350414E3E3C5350414E207374796C653D22464F4E542D53495A453A20313670743B20464F4E542D46414D494C593A20B7C2CBCE5F474232333132223EBAE9BAFECAD0C9ADC1D6B9ABB0B23C2F5350414E3E3C5350414E207374796C653D22464F4E542D53495A453A20313670743B20434F4C4F523A20626C61636B3B20464F4E542D46414D494C593A20B7C2CBCE5F4742323331323B206D736F2D61736369692D666F6E742D66616D696C793A202754696D6573204E657720526F6D616E27223EBACDC9ADC1D6B7C0BBF0B9A4D7F7CBF9C8A1B5C3B5C4B3C9BCA83C2F5350414E3E3C5350414E207374796C653D22464F4E542D53495A453A20313670743B20464F4E542D46414D494C593A20B7C2CBCE5F474232333132223EB8F8D3E8C1CBB3E4B7D6BFCFB6A8A1A33C2F5350414E3E3C5350414E207374796C653D22464F4E542D53495A453A20313670743B20434F4C4F523A20626C61636B3B20464F4E542D46414D494C593A20B7C2CBCE5F4742323331323B206D736F2D61736369692D666F6E742D66616D696C793A202754696D6573204E657720526F6D616E27223EB2A2B6D4BAE9BAFEC9ADC1D6B9ABB0B2CAC2D2B5B7A2D5B9CCE1B3F6C1CBCEE5B5E3BEDFCCE5D2AAC7F3A3BA3C2F5350414E3E3C5350414E207374796C653D22464F4E542D53495A453A20313670743B20464F4E542D46414D494C593A20B7C2CBCE5F474232333132223ED2BBCAC73C2F5350414E3E3C5350414E207374796C653D22464F4E542D53495A453A20313670743B20464F4E542D46414D494C593A20B7C2CBCE5F4742323331323B206D736F2D61736369692D666F6E742D66616D696C793A2056657264616E613B206D736F2D68616E73692D666F6E742D66616D696C793A2056657264616E61223ED2AAB4F3C1A6CDC6BDF8A1B0CEE5BBAFA1B1BDA8C9E8A3ACCCD8B1F0CAC7BEAFCEF1D0C5CFA2BBAFBDA8C9E8BACDB6D3CEE9D5FDB9E6BBAFBDA8C9E8A1A33C2F5350414E3E3C5350414E207374796C653D22464F4E542D53495A453A20313670743B20464F4E542D46414D494C593A20B7C2CBCE5F474232333132223EB6FECAC7D2AAC8CFD5E6C2C4D0D0BAC3D6B0D4F0A3ACBCD3B4F3D6B4B7A8B0ECB0B8C1A6B6C8A3ACCEACBBA4C1D6D2B5C9FACCACB0B2C8ABA3BBC8FDCAC7D2AAC2E4CAB5BAC3B1A3D5CFA3ACD2AAC7D0CAB5B9D8D0C4C3F1BEAFB3C9B3A4A3ACCCE1B8DFC3F1BEAFB4FDD3F6A3BBCBC4CAC7D2AACCE1C9FDD0C5CFA2BBAFCBAEC6BDA3ACB7A2BBD3BEAFD7DBC6BDCCA8D7F7D3C3A3ACD7C5C1A6CDC6BDF8D2B5CEF1D3C3B7BFBDA8C9E8A1A3CEE5CAC7D2AABCCCD0F8D7A5BAC3C9ADC1D6B7C0BBF0D6B5B0E0B9A4D7F7A3ACC2E4CAB5BAC3C9ADC1D6B7C0BBF0B8F7CFEED6C6B6C8A3ACD5F9C8A1B3C9CEAAC8ABCAA1C9ADC1D6B7C0BBF0CFC8BDF8B5A5CEBBA1A33C42207374796C653D226D736F2D626964692D666F6E742D7765696768743A206E6F726D616C223EA3A8BEA3D6DDCAD0C9ADC1D6B9ABB0B2BED6A3A93C2F423E3C5350414E206C616E673D454E2D55533E3C6F3A703E3C2F6F3A703E3C2F5350414E3E3C2F5350414E3E3C2F503E,
#     '2011-12-16 16:09:05',
#     '1322116100421.html',
#     null, null, null, null, null, null, null, null, null, null, null, 
#     '湖北森林公安网',  
#     '2011-12-13 17:41:46',
#     '管理员', null, null, '1', '超级管理员', '2011-12-16 16:38:14', null,
#     '2011-12-26 17:57:45', '0', null, null, '583', null, null, null, null, null, null);


# vweb_filetransfer  文件报送表
# vweb_log  操作日志表
# vweb_media   影像资料
# vweb_message  天气信息表
# vweb_navigation  网站导航记录表
# vweb_news_list   文章列表
# vweb_news_list_zt   文章签收信息表
# vweb_org  部门机构
# vweb_person   人员表
# vweb_person_role   用户--角色
# vweb_picnews_list   图片新闻列表
# vweb_privilegle   功能列表
# vweb_reflect    情况反映
# vweb_role   角色表
# vweb_role_privilege   角色--模块表
# vweb_software    常用软件信息表
# vweb_subject    专题展示表
# vweb_template   文章模版信息
# vweb_tree_dict   栏目信息表
# vweb_visitlog   网站访问量统计
# vweb_weather   天气信息表




