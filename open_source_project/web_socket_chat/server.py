from pywss import Pyws, route, json, ConnectManager


@route('/ws/chat')  # 注册path
def ws_chat(request, data):
    json_data = json.loads(data)
    if json_data.get('start') == True:  # 接收start指令
        # 更新所有已建立连接的socket的当前在线人数
        request.conn.send_to_all({'online': ConnectManager.online()})
        return {'sock_id': request.conn.name}  # 返回自身唯一sock_id
    msg = json_data.get('msg')
    if msg:  # 获取聊天消息，发送给所有已建立连接的socket
        request.conn.send_to_all({'from': request.conn.name, 'msg': msg})


if __name__ == '__main__':
    ws = Pyws(__name__, address='127.0.0.1', port=8868)
    ws.serve_forever()
