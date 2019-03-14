import json


def reduce_content(data):
    '''
    Reduce  json content with specific structure:
    e.g.: {'id': 'BOX_REGISTER_NEW_DEVICE', 'param': ['no_scan', 'CloudEdge_95']}
    '''
    str_len, basic_str_len, max_len = 0, 0, 1024
    data_str = json.dumps(data)
    if len(data_str) < max_len:
        return data
    basic_str_len = len('{}') + len('"id": ') + len('""') + len(data['id']) \
        + len(', ') + len('"param": ') + len('[]')
    str_len = basic_str_len
    for idx in range(len(data['param'])):
        item = data['param'][idx]
        if idx == 0:
            item_len = len(item) + len('""')
        else:
            item_len = len(', ') + len('""') + len(item)
        if item_len + str_len > max_len:
            if idx == 0:
                sleft = max_len - str_len - len('""')
            else:
                sleft = max_len - str_len - len('""') - len(', ')
            print str_len, item_len, sleft
            data['param'][idx] = data['param'][idx][:sleft]
            print data['param'][idx]
            return data
        str_len += item_len
    return data


if __name__ == '__main__':
    data = {"id":"ADD_WHITE_LIST","param":["www.google1.com,www.google2.com,www.google3.com,www.google4.com,www.google5.com,www.google6.com,www.google7.com,www.google8.com,www.google9.com,www.google10.com,www.google11.com,www.google12.com,www.google13.com,www.google14.com,www.google15.com,www.google16.com,www.google17.com,www.google18.com,www.google19.com,www.google20.com,www.google21.com,www.google22.com,www.google23.com,www.google24.com,www.google25.com,www.google26.com,www.google27.com,www.google28.com,www.google29.com,www.google30.com,www.google31.com,www.google32.com,www.google33.com,www.google34.com,www.google35.com,www.google36.com,www.google37.com,www.google38.com,www.google39.com,www.google40.com,www.google41.com,www.google42.com,www.google43.com,www.google44.com,www.google45.com,www.google46.com,www.google47.com,www.google48.com,www.google49.com,www.google50.com,www.google51.com,www.google52.com,www.google53.com,www.google54.com,www.google55.com,www.google56.com,www.google57.com,www.google58.com,www.google...aaaeff"]}
    data = {"id":"ADD_WHITE_LIST","param":["www.google1.com,www.google2.com,www.google3.com,www.google4.com", "www.google5.com,www.google6.com,www.google7.com,www.google8.com,www.google9.com,www.google10.com,www.google11.com,www.google12.com,www.google13.com,www.google14.com,www.google15.com,www.google16.com,www.google17.com,www.google18.com,www.google19.com,www.google20.com,www.google21.com,www.google22.com,www.google23.com,www.google24.com,www.google25.com,www.google26.com,www.google27.com,www.google28.com,www.google29.com,www.google30.com,www.google31.com,www.google32.com,www.google33.com,www.google34.com,www.google35.com,www.google36.com,www.google37.com,www.google38.com,www.google39.com,www.google40.com,www.google41.com,www.google42.com,www.google43.com,www.google44.com,www.google45.com,www.google46.com,www.google47.com,www.google48.com,www.google49.com,www.google50.com,www.google51.com,www.google52.com,www.google53.com,www.google54.com,www.google55.com,www.google56.com,www.google57.com,www.google58.com,www.google...aaaeff"]}
    data = {"id":"AADD_WHITE_LISTDD_WHITE_LIST","param":["www.google1.com,www.ggoogle2google2google2google2google2google2oogle2.com,www.google3.com,www.google4.com", "www.google5.com,www.google6.com,www.google7.com,www.google8.com,www.google9.com,www.google10.com,www.google11.com,www.google12.com,www.google13.com,www.google14.com,www.google15.com,www.google16.com,www.google17.com,www.google18.com,www.google19.com,www.google20.com,www.google21.com,www.google22.com,www.google23.com,www.google24.com,www.google25.com,www.google26.com,www.google27.com,www.google28.com,www.google29.com,www.google30.com,www.google31.com,www.google32.com,www.google33.com,www.google34.com,www.google35.com,www.google36.com,www.google37.com,www.google38.com,www.google39.com,www.google40.com,www.google41.com,www.google42.com,www.google43.com,www.google44.com,www.google45.com,www.google46.com,www.google47.com,www.google48.com,www.google49.com,www.google50.com,www.google51.com,www.google52.com,www.google53.com,www.google54.com,www.google55.com,www.google56.com,www.google57.com,www.google58.com,www.google...aaaeff"]}
    data = {"id":"AADD_WHITE_LISTDD_WHITE_LIST","param":["www.google1.com,wwwm", "wm,www.google10.com,www.google11.com,www.google12.com,www.google13.com,www.google14.com,www.google15.com,www.google16.com,www.google17.com,www.google18.com,www.google19.com,www.google20.com,www.google21.com,www.google22.com,www.google23.com,www.google24.com,www.google25.com,www.google26.com,www.google27.com,www.google28.com,www.google29.com,www.google30.com,www.google31.com,www.google32.com,www.google33.com,www.google34.com,www.google35.com,www.google36.com,www.google37.com,www.google38.com,www.google39.com,www.google40.com,www.google41.com,www.google42.com,www.google43.com,www.google44.com,www.google45.com,www.google46.com,www.google47.com,www.google48.com,www.google49.com,www.google50.com,www.google51.com,www.google52.com,www.google53.com,www.google54.com,www.google55.com,www.google56.com,www.google57.com,www.google58.com,www.google...aaaeff"]}
    data = {"id":"ADD_WHITE_LIST","param":["*download.windowsupdate.com\/*,download.microsoft.com\/*,*update.microsoft.com\/*,*windowsupdate.com\/*,*.google.com\/*,ntservicepack.microsoft.com\/*,wustat.windows.com\/*,*.trendmicro.co.jp\/*,*.trendmicro.com\/*,*.trendmicro.org\/*,*windowsupdate.microsoft.com\/*,*.apple.com\/*,www.112211312312312312312312312312312312312312312312313123333333333333333333333333333333333333333333333333333333333333312312312313131313131231312313131313131312313131312313131313131212312313123131231111111111111111111111111111111111231312312311.com\/*,www.1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111asdfadasdfafdasfsafasfafafafafadfaf.com\/*,www.adfasdfasdfadfasdfdadfadfadfafaafdfaafafafsfasdfadfafadfadfadfdafdadfasfasdfasdfasdfasdfafdsdfadfasdfasdfasdfasdfasfasdfasdfasdfasdfasdfafdadfdadsfasdfa23131312sdfafafaefaefaefadfafeafaefasdfaefasdfaefasdfawefcvzcvdadfafefvvzcvzvadfasfsadfa.com\/*,wwwwdfasdfasdfadfkajfajsdfashdfkdhskfhakhfkashdfkajhdfkhadkfhaldjfhalksdfhakjdshkashdkfjahklhakdhfjahdlfhajhfahdsfjlahdflkahdkfjahkdjhfakjdhfkasdhfkasjdhfakdhfkajdhfkasdhfklasdjhfkldjjkkjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjdddd.com\/*,www.wdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddfwwwwwwwwwewrwrwefdfadsfasdfasdfffffffffffffffffffffeffasdfadfasdfasfasdfsdfafsdafadfasdfdfadfafsfasdfafasdfadfasdfadfafsdfds31312313123.com.com\/*","URL"]}
    data = {"id":"ADD_WHITE_LIST","param":["*download.windowsupdate.com\/*,download.microsoft.com\/*,*update.microsoft.com\/*,*windowsupdate.com\/*,*.google.com\/*,ntservicepack.microsoft.com\/*,wustat.windows.com\/*,*.trendmicro.co.jp\/*,*.trendmicro.com\/*,*.trendmicro.org\/*,*windowsupdate.microsoft.com\/*,*.apple.com\/*,www.112211312312312312312312312312312312312312312312313123333333333333333333333333333333333333333333333333333333333333312312312313131313131231312313131313131312313131312313131313131212312313123131231111111111111111111111111111111111231312312311.com\/*,www.1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111asdfadasdfafdasfsafasfafafafafadfaf.com\/*,www.adfasdfasdfadfasdfdadfadfadfafaafdfaafafafsfasdfadfafadfadfadfdafdadfasfasdfasdfasdfasdfafdsdfadfasdfasdfasdfasdfasfasdfasdfasdfasdfasdfafdadfdadsfasdfa23131312sdfafafaefaefaefadfafeafaefasdfaefasdfaefasdfawefcvzcvdadfafefvvzcvzvadfasfsadfa.com\/*,wwwwdfasdfasdfadfkajfajsdfashdfkdhskfhakhfkashdfkajhdfkhadkfhaldjfhalksdfhakjdshkashdkfjahklhakdhfjahdlfhajhfahdsfjlahdflkahdkfjahkdjhfakjdhfkasdhfkasjdhfakdhfkajdhfkasdhfklasdjhfkldjjkkjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjdddd.com\/*,www.wdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddfwwwwwwwwwewrwrwefdfadsfasdfasdfffffffffffffffffffffeffasdfadfasdfasfasdfsdfafsdafadfasdfdfadfafsfasdfafasdfadfasdfadfafsdfds31312313123.com.com\/*"]}
    print json.dumps(data)
    print len(json.dumps(data))
    ret_data = reduce_content(data)
    print json.dumps(ret_data)
    print len(json.dumps(ret_data))
