import React, {useCallback, useContext, useEffect} from 'react'
import LoadingSpinner1 from '../loadingAndErrors/LoadingSpinner1'
import { Link, useHistory} from 'react-router-dom'
import Button3 from '../buttonsAndInputs/Button3'
import Button4 from '../buttonsAndInputs/Button4'
import SocketContext from '../../context/SocketContext'
import AuthContext from '../../context/AuthContext'

import { CountRenders } from '../../utils/CountRenders'

const LockControls = ({device}) => {
    const {socketConnected, socket, currentDevice, currentDeviceStatus} = useContext(SocketContext)
    const {User} = useContext(AuthContext)
    const history = useHistory()


    CountRenders('lock controls: ')

    const pingLock = useCallback(() => {
        if (!socketConnected) return
        //send requesting user id in action section for pong from device
        const payload = JSON.stringify({
            type:'ping',
            action:User.id,
            status:false,
            unit_id:device.unit_id,
            unit_ip_url:false,
            image:false,
        })
        socket.current.send(payload)
    }, [currentDevice])

    const sendCommand = () => {
        const action = currentDevice.current.status === 'locked' ? 'unlock' : 'lock'
        const payload = JSON.stringify({
            type:'command',
            action:action,
            unit_id:device.unit_id,
            unit_ip_url: false,
            image: false,
        })
        socket.current.send(payload)
    }

    useEffect(() => {
        if(!currentDevice.current) return
        pingLock()

    }, [socketConnected, pingLock, currentDevice])


  return (
    <div  className='w-100 justify-content-space-around padding-10'>
        <Link to={`/edit/${device.id}`}>
          <Button3
          text='Edit'
          action={() => {history.push(`edit/${device.id}`)}}
          />
        </Link>
        
        {currentDevice.current && currentDevice.current.unit_id === device.id && 
        currentDeviceStatus ?
            <Button4
            text={currentDeviceStatus === 'locked' ? 'Unlock' : 'Lock'}
            action={sendCommand}
            />

            :

            <Button4
            text={<LoadingSpinner1 size='lds-btn-size' />}
            action={pingLock}
            />
        }
        
  </div>
  )
}

export default LockControls
