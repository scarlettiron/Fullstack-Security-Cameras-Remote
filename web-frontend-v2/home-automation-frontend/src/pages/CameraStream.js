import React, {useEffect, useContext, useState} from 'react'
import SocketContext from '../context/SocketContext'
import Button2 from '../components/buttonsAndInputs/Button2'
import {ReactComponent as ArrowBack} from '../assets/left-chevron.svg'
import { useParams } from 'react-router-dom'
import FormatSocketPayload from '../utils/FormatSocketPayload'
import StreamImg from '../components/StreamImg'
import { useHistory } from 'react-router-dom'
import { CountRenders } from '../utils/CountRenders'
import '../css/stream.css'
import '../css/general.css'


const CameraStream = () => {
  const {socket, socketConnected, handleSetCurrentDevice, handleStopStream} = useContext(SocketContext)
  const {unit_id} = useParams()
  const history = useHistory()
  const [error, setError] = useState(() => false)

  CountRenders('Camera stream: ')

  // request for server to start stream
  const requestStream = () => {
    if(!socketConnected){
      setError('Error comunicating with server')
      return
    }
    const payload = FormatSocketPayload({type:'stream', unit_id:unit_id, action:'request'})
    socket.current.send(payload)
  }

  //push current camera into array stored in local storage for later cleanup code
  const addCameraToLocalStorage = () => {
    let cams = []
    if(localStorage.getItem('active-camera-streams')){
      cams = JSON.parse(localStorage.getItem('active-camera-streams'))
    }

    cams.push(unit_id)
    localStorage.setItem('active-camera-streams', JSON.stringify(cams))
  }

  const leaveStream = () => {
    handleStopStream()
    history.goBack()
  }

  useEffect(()=>{
    const setup = async () => {
      await handleSetCurrentDevice(unit_id, true, 'streaming')
      requestStream()
      addCameraToLocalStorage()
    }
    setup()

  })

  return (
    <div className='stream-page-container'>
        <div className='stream-controls'>
          <Button2 text={<ArrowBack className='svg1'/>} action={leaveStream}/>
        </div>
          <StreamImg/>
    </div>

  )
}

export default CameraStream