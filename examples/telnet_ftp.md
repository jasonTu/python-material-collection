
## Referer
* [Windows 下使用ftp批处理脚本][1]
* [windows7无法启动Telnet服务，出现错误1068][2]
* [python telnet连接到windows方法][3]
* [Telnet远程操作Windows服务器][4]

[1]: https://blog.csdn.net/oscar999/article/details/45074679
[2]: http://blog.sina.com.cn/s/blog_866c5a5d0101as9k.html
[3]: https://blog.csdn.net/yingzinanfei/article/details/53165819
[4]: https://blog.csdn.net/weiyi556/article/details/54612754


```python
import telnetlib
```


```python
tn = telnetlib.Telnet('192.168.1.55')
```


```python
tn.read_until(b'login: ')
```




    b'Welcome to Microsoft Telnet Service \r\n\n\rlogin: '




```python
tn.write(b'xman\r\n')
```


```python
tn.read_until(b'password: ')
```




    b'xman\n\rpassword: '




```python
tn.write(b'111111\r\n')
```


```python
for i in range(5):
    tn.read_until(b'\n', 2)
```


```python
tn.read_until(b'>', 2)
```




    b'C:\\Users\\xman>'




```python
tn.write(b'echo open 192.168.1.202 >> ftptmp.txt\r\n')
tn.write(b'echo user ftpadmin 111111 >> ftptmp.txt\r\n')
tn.write(b'echo get 10.txt >> ftptmp.txt\r\n')
tn.write(b'echo bye >> ftptmp.txt\r\n')
tn.write(b'echo exit >> ftptmp.txt\r\n')
```


```python
while True:
    if tn.read_until(b'\n', 2) == b'':
        break
```


```python
tn.write(b'ftp -n -s:"ftptmp.txt"\r\n')
```


```python
while True:
    if tn.read_until(b'\n', 2) == b'':
        break
```


```python
tn.close()
```
