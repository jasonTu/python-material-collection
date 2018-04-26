

```python
import paramiko
```


```python
transport = paramiko.Transport(('192.168.1.153',50001))  
```


```python
transport.connect(username='root',password='puyacn#1..')  
```


```python
sftp = paramiko.SFTPClient.from_transport(transport)  
```


```python
lfile = '/root/suspects_uploader.bat'
```


```python
sftp.put(lfile, '/tmp/suspects_uploader.bat2')
```




    <SFTPAttributes: [ size=1802 uid=0 gid=0 mode=0o100644 atime=1524711914 mtime=1524711914 ]>




```python
dir(sftp)
```




    ['__class__',
     '__delattr__',
     '__dict__',
     '__dir__',
     '__doc__',
     '__enter__',
     '__eq__',
     '__exit__',
     '__format__',
     '__ge__',
     '__getattribute__',
     '__gt__',
     '__hash__',
     '__init__',
     '__le__',
     '__lt__',
     '__module__',
     '__ne__',
     '__new__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__setattr__',
     '__sizeof__',
     '__str__',
     '__subclasshook__',
     '__weakref__',
     '_adjust_cwd',
     '_async_request',
     '_convert_status',
     '_cwd',
     '_expecting',
     '_finish_responses',
     '_lock',
     '_log',
     '_read_all',
     '_read_packet',
     '_read_response',
     '_request',
     '_send_packet',
     '_send_server_version',
     '_send_version',
     '_transfer_with_callback',
     '_write_all',
     'chdir',
     'chmod',
     'chown',
     'close',
     'file',
     'from_transport',
     'get',
     'get_channel',
     'getcwd',
     'getfo',
     'listdir',
     'listdir_attr',
     'listdir_iter',
     'logger',
     'lstat',
     'mkdir',
     'normalize',
     'open',
     'posix_rename',
     'put',
     'putfo',
     'readlink',
     'remove',
     'rename',
     'request_number',
     'rmdir',
     'sock',
     'stat',
     'symlink',
     'truncate',
     'ultra_debug',
     'unlink',
     'utime']




```python
sftp.mkdir('/tmp/remote_mk_dir')
```


```python
ssh = paramiko.SSHClient()
```


```python
ssh.load_system_host_keys()  
```


```python
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
```


```python
ssh.connect(hostname='192.168.1.153', port=50001, username='root', password='puyacn#1..')  
```


```python
stdin, stdout, stderr = ssh.exec_command('ls') 
```


```python
stdout
```




    <paramiko.ChannelFile from <paramiko.Channel 1 (closed) -> <paramiko.Transport at 0x60144f98 (cipher aes128-ctr, 128 bits) (active; 0 open channel(s))>>>




```python
print(stdout.read())
```

    b'anaconda-ks.cfg\ninstall.log\ninstall.log.syslog\nPython-3.6.5\nPython-3.6.5.tar.xz\nwebshell-sample-master\nwebshell-sample-master.zip\n'



```python
ssh.close()
```
