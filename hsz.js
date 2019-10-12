const electron = require('electron');
const {
    webContents
} = require('electron');
const {
    session
} = require('electron');
const {
    dialog
} = require('electron');
const {
    autoUpdater
} = require('electron-updater');

const BrowserWindow = electron.BrowserWindow;
const Menu = electron.Menu;
const app = electron.app;
const path = require('path');
const ipc = require('electron').ipcMain;
let projectName = "慧算账";
let projectIco = "ico_tph.ico";
let projectUrl = "https://sap.kungeek.com/portal/ftsp/portal/home.do?main";

let template = [{
    id:1,
            label: '返回',
            click: function (item, focusedWindow) {
                if (focusedWindow) {
                    focusedWindow.webContents.goBack()
                }
            }
        }, {id:2,
            label: '前进',
            click: function (item, focusedWindow) {
                if (focusedWindow) {
                    focusedWindow.webContents.goForward()
                }
            }
        }, {id:3,
            label: '刷新',
            accelerator: 'F5',
            click: function (item, focusedWindow) {
                if (focusedWindow) {
                    // 重载之后, 刷新并关闭所有的次要窗体
                    if (focusedWindow.id === 1) {
                        BrowserWindow.getAllWindows().forEach(function (win) {
                            if (win.id > 1) {
                                win.close()
                            }
                        })
                    }
                    focusedWindow.reload()
                }
            }
        },{
    id:4,
            label: '控制台',
            accelerator: 'F6',
            click: function (item, focusedWindow) {
                if (focusedWindow) {
                    BrowserWindow.getFocusedWindow().webContents.openDevTools()
                }
            }
        }];

function createWindow() {
    // 创建浏览器窗口。
    win = new BrowserWindow({
        width: 1300,
        height: 766,
        autoHideMenuBar: false,
        title: projectName,
        icon: projectIco,
        webPreferences: {
            webSecurity: false,
        }
    })
    win.loadURL(projectUrl);
    win.webContents.on('did-finish-load', (event, url) = > {
        //判断是否是登陆状态
        backdata=0;
    win.webContents.executeJavaScript(`
        getAllzt=function () {
            var params = {} ;
            params.url = 'https://sap.kungeek.com/portal/ftsp/portal/form.do?getAllCustomers' ;
            params.data = {pageIndex: 1, pageSize: 10000};
            params.callback = function(result){
                if(result.success) {
                    top.zt_data = result.data;
                } else {
                    top.zt_data = result.errMsg;
                }
            }
            ftsps.ajax.postData(params) ;
        }
                function Ajax_post(data,url){
                $.ajax({
                         async: false,
                         type: "post",
                         data: data,
                         url: url,
                         fail:function(data){
                         alert('后台报错,请稍后在使用');
                         },success: function(data) {
                           if ('tasking'==data){ //任务开始
                            localStorage.setItem('task_start', 1)
                            }
                           else if ('next_month'==data){
                           alert('本月没有待执行任务,准备退出账号')
                           localStorage.clear()
                           document.location.href='https://sap.kungeek.com/portal/j_spring_security_logout'
                           }
                           else if ('task_accomplish'==data){
                           localStorage.setItem('task_accomplish',1)
                           }
                           else if ('task_working'==data){
                           localStorage.setItem('task_working',1)
                           }
                           else if ('task_failed'==data){
                            if (localStorage.task_filed>2){
                            alert('任务尝试多次失败,请稍候重试或联系后台')
            document.location.href='https://sap.kungeek.com/portal/j_spring_security_logout'
            }
            else if (localStorage.task_filed==undefined){
                localStorage.setItem('task_filed',1)}
                alert('任务尝试失败1次,请重新登录')
                document.location.href='https://sap.kungeek.com/portal/ftsp/portal/home.do?main'+'&useridx='+$.DEFAULTS.userId
            }}
                         }
                )}
            if ($.DEFAULTS.userId && localStorage.task_start!=1 && document.location.href.indexOf('login')==-1){
            suffix='userId='+$.DEFAULTS.userId
            url="http://127.0.0.1:5060/distribute?"+suffix
            getAllzt()
            data=JSON.stringify({"zt_data":top.zt_data})
            Ajax_post(data,url)
            document.location.href='https://sap.kungeek.com/portal/ftsp/portal/home.do?main'+'&useridx='+$.DEFAULTS.userId}    
            if (localStorage.tasking==1){
            //每1分钟轮训一次：
            function countSecond() {
            suffix='userId='+$.DEFAULTS.userId+'&userName='+$.DEFAULTS.userName+'&zjxxName='+$.DEFAULTS.zjxxName　
            url="http://127.0.0.1:5060/task_state?"+suffix
            Ajax_post(data,url)
            i=setTimeout("countSecond()", 10000 )
            if (localStorage.task_accomplish==1){
            clearTimeout(i)
            backdata=1000000000
            alert('任务已完成,准备退出账号')
            }
            else if (localStorage.task_working==1){
            console.log('任务中,请稍后')
            }
            }
            }
        `, true).then((result) = > {if(backdata > 999999
)
    {
        //如果大于999999
        win2.webContents.executeJavaScript(`
            alert('所有账套数据入库成功')
            localStorage.clear()
            document.location.href='https://sap.kungeek.com/portal/j_spring_security_logout'
           `)
    }
})
});
    win.webContents.openDevTools()
}



//app.commandLine.appendSwitch("--disable-http-cache");
app.commandLine.appendSwitch('proxy-server', '116.228.76.168:7777');
app.commandLine.appendSwitch('disable-background-timer-throttling');
app.commandLine.appendSwitch('--disable-web-security');

app.on('ready', function () {
    const menu = Menu.buildFromTemplate(template);
    Menu.setApplicationMenu(menu);
    createWindow()
});

app.on('activate', () => {
    if (win === null) {
        createWindow()
    }
});