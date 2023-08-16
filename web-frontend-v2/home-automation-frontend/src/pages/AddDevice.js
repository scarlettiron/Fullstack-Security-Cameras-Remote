import React, {useState, useContext} from 'react'
import { useHistory } from 'react-router-dom'
import AuthContext from '../context/AuthContext'
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

const AddDevice = () => {
    const history = useHistory()
    const {detailUpdateDevice} = deviceUrls
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [success, setSuccess] = useState(null)

    const {User} = useContext(AuthContext)

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
        console.log(unit_id)
        console.log(name)
        if(!unit_id || !name){
            setError('Please provide valid unit_id and unit name')
            return
        } 
        const fetchConfig = {method:'PUT', body:JSON.stringify({
            household:User.household,
            name:name
        }), signal:signal}

        const {response, data} = await CustomFetch(`${detailUpdateDevice.url}${unit_id}/`, fetchConfig)
        if(response.status === 201){
            setLoading(false)
            setSuccess(true)
        }
        else{
            setError(data)
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
                    <h3 className='text-white'>Add A New Device</h3>
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
                        placeholder={'Name Unit (Back Door Camera)'}
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

export default AddDevice