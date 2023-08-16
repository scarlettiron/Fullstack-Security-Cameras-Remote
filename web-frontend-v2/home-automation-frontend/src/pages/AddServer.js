import React, {useState, useContext} from 'react'
import { useHistory } from 'react-router-dom'
import AuthContext from '../context/AuthContext'
import DeviceContext from '../context/DeviceContext'
import Input from '../components/buttonsAndInputs/Input'
import SideBar from '../components/navbars/SideBar'
import Button3 from  '../components/buttonsAndInputs/Button3'
import Button4 from  '../components/buttonsAndInputs/Button4'
import LoadingSpinner1 from '../components/loadingAndErrors/LoadingSpinner1'
import '../css/edit-add-device.css'
import '../css/general.css'
import CustomFetch from '../utils/CustomFetch'
import { deviceUrls } from '../utils/ApiEndpoints'
import Error1 from '../components/loadingAndErrors/Error1'
import Success1 from '../components/loadingAndErrors/Success1'

const AddServer = () => {
    const history = useHistory()
    const {localServerDetail} = deviceUrls
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [success, setSuccess] = useState(null)

    const {User} = useContext(AuthContext)
    const {addServerToState} = useContext(DeviceContext)

    const controller = new AbortController()
    const signal = controller.signal

    const handleAbort = () => {
        controller.abort()
        setLoading(false)
    }

    const handleAddDevice = async (e) => {
        e.preventDefault()
        setError(null)
        const unit_id = e.target.unit_id.value
        const name = e.target.name.value

        if(!unit_id || !name){
            setError('Please provide valid unit_id and unit name')
            return
        } 
        const fetchConfig = {method:'PUT', body:JSON.stringify({
            household:User.household,
            name:name, 
        }), signal:signal}

        const {response, data} = await CustomFetch(`${localServerDetail.url}${unit_id}/`, fetchConfig)
        if(response.status === 200){
            console.log(data)
            console.log(data.id)
            addServerToState(data)
            setLoading(false)
            setSuccess(true)
        }
        else{
            setError("unable to add server, try again later")
            setLoading(false)
        }
    }

  return (
    <div className='w-100'>
        <SideBar/>
        <div className='container'>
            {success &&
                <Success1/>
            }
            {!success &&
                <form className='add-device-container' method='PUT' 
                onSubmit={handleAddDevice} id='addDeviceForm'>
                    <h3 className='text-white'>Add A New Home Server</h3>
                    <div className='w-100 justify-content-center'>
                        <p className='text-white'>A server is a main "hub" all the devices in your household
                        connect to in order to be able to communicate with eachother and perform remote actions</p>
                    </div>
                    {error &&
                        <Error1 message={error} wrapperClass={'w-75 justify-content-center'}/>
                    }
                    <div className='w-75'>
                        <Input 
                        id='unit_id'
                        placeholder='Enter Unit ID'
                        />
                    </div>
                    <div className='w-75'>
                        <Input
                        id='name'
                        placeholder={'Name Unit (Home Server, Workshop Server)'}
                        />
                    </div>
                    <div className='justify-content-between w-75 padding-10 margin-10'>
                        <Button3 text='Cancel' action={loading ? handleAbort : () => {history.goBack()}} />
                        <Button4 text={loading ? <LoadingSpinner1 size='lds-btn-size' /> : 'Add'}
                        type='submit' form={loading ? null : 'addDeviceForm'}
                        />
                    </div>
                </form>
            }
        </div>
    </div>
  )
}

export default AddServer