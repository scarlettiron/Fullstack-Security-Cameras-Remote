import React, {createContext, useEffect, useRef, useState, useContext} from 'react'
import { w3cwebsocket as w3cSocket } from "websocket"
import AuthContext from './AuthContext'
import FormatSocketPayLoad from '../utils/FormatSocketPayload';

const SocketContext = createContext()
export default SocketContext;

export const SocketProvider = ({children}) => {
    const {User, loginUser} = useContext(AuthContext)

    ///!!! Change to householdid !!!///
    const socketServerUrl = 'ws://127.0.0.1:8000/ws/routing/1/'
    const socket= useRef()
    const [socketConnected, setSocketConnected] = useState(() => false)

    //for camera frames from devices
    const [frame, setFrame] = useState(() => null)
    const handleVideoFrame = (image) => {
        let orgImg = image.slice(0, image.length - 1).slice(2)
        setFrame(`data:image/jpg;base64,${orgImg}`)
    }


    //for keeping track of unit currently being accessed
    const currentDevice = useRef()
    const [currentDeviceStatus, setCurrentDeviceStatus] = useState()

    const handleSetCurrentDevice = async (unit_id, online, status) => {
        //if(!allDevices.includes(unit_id)) return
        currentDevice.current = {'unit_id':unit_id, 'online':online, 'status':status}
        setCurrentDeviceStatus(status)
    }

    //get list of units from local storage that have been viewed and end all streams
    const handleStopStream = async () => {
        const cams = JSON.parse(localStorage.getItem('active-camera-streams'))
        if(cams.length > 0){
            const payload = FormatSocketPayLoad({
                'type':'stream',
                'action':'end',
                'unit_id':cams
            })
            await socket.current.send(payload)
            setFrame(null)
            currentDevice.current = null
        }
    }

    // this is used for updating users home server when a new person
    // is added for facial recognition
    const handleUpdateHomeServerPersons = async () => {
        if(!socketConnected) return

        const payload = FormatSocketPayLoad({
            'type':'command',
            'action':'update persons',
            'unit_id': 'all'
        })

        await socket.current.send(payload)
    }

    const handleParsedData = (data) => {
        switch(data.type){
            case 'stream':
                if (data.image){
                    //logic to stop cam streaming if no longer viewing
                    const path = window.location.pathname
                    if(!path.includes('camera')){
                        handleStopStream()
                    }
                    //for multiple server connections
                    //make sure unit_id from socket matches current viewed camera
                    if(data.unit_id === currentDevice.current.unit_id){
                        handleVideoFrame(data.image)
                    }
                }
                break
            case 'pong':
                if(data.unit_id === currentDevice.current['unit_id']){
                    //in this instance, data.action containes the status of the lock(locked or unlocked)
                    handleSetCurrentDevice(data.unit_id, true, data.status)
                }
                break
            default:
                return
        }
    }


    useEffect(()=>{
        //if person is not logged in return
        if(!User) return

        // to avoid multiple sockets from being opened
        if(socketConnected === true) return

        const newSocket = new w3cSocket(socketServerUrl)

        newSocket.onerror = (error) => {
            setSocketConnected(false)
            newSocket.close()
        }

        newSocket.onclose = () => {
            setSocketConnected(false)
            console.log('socket closed')
        }

        newSocket.onopen = () => {
            console.log('socket open')
            setSocketConnected(true)
        }

        newSocket.onmessage = ({data}) => {
        console.log(data)
            let parsedData = JSON.parse(data)
            console.log(parsedData)
            handleParsedData(parsedData)
        }

        socket.current = newSocket

        return () => socket.current.close()

    },[setSocketConnected, loginUser. socketConnected, User])



    const socketContextData = {
        socket:socket,
        socketConnected:socketConnected,
        frame:frame,
        currentDevice:currentDevice,
        currentDeviceStatus:currentDeviceStatus,
        handleSetCurrentDevice:handleSetCurrentDevice,
        handleStopStream:handleStopStream,
        handleUpdateHomeServerPersons:handleUpdateHomeServerPersons,
    }

  return (
    <SocketContext.Provider value={socketContextData}>
        {children}
    </SocketContext.Provider>
  )
}

