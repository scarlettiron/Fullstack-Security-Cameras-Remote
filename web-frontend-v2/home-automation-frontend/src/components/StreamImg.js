import React, {useContext} from 'react'
import SocketContext from '../context/SocketContext'
import LoadingSpinner1 from '../components/loadingAndErrors/LoadingSpinner1'
import '../css/stream.css'
import '../css/general.css'

const StreamImg = () => {
    const {frame} = useContext(SocketContext)
  return (
    <div className='stream-container'>
        {frame ?
        <img src={frame} alt={'camera stream'} className='stream-frame'/>
        :
          <LoadingSpinner1 />
        }
    </div>
  )
}

export default StreamImg