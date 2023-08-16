import React, {useState, useContext} from 'react'
import { useHistory } from 'react-router-dom'
import SocketContext from '../context/SocketContext'
import AuthContext from '../context/AuthContext'
import Input from '../components/buttonsAndInputs/Input'
import SideBar from '../components/navbars/SideBar'
import Button3 from  '../components/buttonsAndInputs/Button3'
import Button4 from  '../components/buttonsAndInputs/Button4'
import FileInput from '../components/buttonsAndInputs/FileInput'
import LoadingSpinner1 from '../components/loadingAndErrors/LoadingSpinner1'
import CustomFetch from '../utils/CustomFetch'
import { allowed_persons } from '../utils/ApiEndpoints'
import Error1 from '../components/loadingAndErrors/Error1'
import Success1 from '../components/loadingAndErrors/Success1'
import '../css/edit-add-device.css'
import '../css/general.css'

const AddAllowedPerson = () => {
    const history = useHistory()
    const {getAllAllowedPersons} = allowed_persons
    const [loading, setLoading] = useState(() => false)
    const [error, setError] = useState(() => null)
    const [success, setSuccess] = useState(() => null)
    const [thumbnail, setThumbnail] = useState(() => null)

    const {User} = useContext(AuthContext)
    const {handleUpdateHomeServerPersons} = useContext(SocketContext)

    const controller = new AbortController()
    const signal = controller.signal

    const handleAbort = () => {
        controller.abort()
        setLoading(false)
    }

    const handleUpdatePicState = (e) => {

        const file = e.target.files[0]
        const filePath = URL.createObjectURL(file)

        const newState = {
            'file':file,
            'path':filePath, 
        }

        setThumbnail(()=>newState)
    }

    const handleAddPerson = async (e) => {
        e.preventDefault()
        setError(null)
        setLoading(true)
        const name = e.target.name.value

        if(!thumbnail || !name){
            setError('Please provide valid name and photo')
            return
        } 

        const payload = new FormData()

        payload.append('name', name)
        payload.append('pic', thumbnail.file)
        payload.append('household', User.household)

        const fetchConfig = {method:'POST', body:payload, signal:signal}

        const {response, data} = await CustomFetch(`${getAllAllowedPersons.url}${User.household}/`, fetchConfig, true)
        if(response.status === 201){
            await handleUpdateHomeServerPersons()
            setLoading(false)
            setSuccess(true)
        }
        else{
            setError(data)
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
                onSubmit={handleAddPerson} id='addPersonForm'>
                    <h3 className='text-white'>Add A New Person</h3>
                    <div className='w-100 justify-content-center'>
                        <p className='text-white'>Add a new allowed person to household. People added to your households
                            "Allowed People List" will not trigger alerts by facial recognition used
                            by camera's. (Photograph of person required)
                        </p>
                    </div>
                    {error &&
                        <Error1 message={error} wrapperClass={'w-75 justify-content-center'}/>
                    }
                    <div className='w-75'>
                        <Input 
                        id='name'
                        placeholder='Name of person'
                        />
                    </div>
                    <div className='w-75 justify-content-center flex-wrap padding-10'>
                        <div className='w-100'>
                            <FileInput 
                            id={'pic'} 
                            onChange={handleUpdatePicState}
                            />
                        </div>
                        <p className='text-white'>Person must be facing camera straight forward.</p>
                    </div>
                    {thumbnail && thumbnail.path &&
                        <img alt='new person' src={thumbnail.path} className='allowed-person-image'/>
                    }
                    <div className='justify-content-between w-75 padding-10 margin-10'>
                        <Button3 text='Cancel' action={loading ? handleAbort : () => {history.goBack()}} />
                        <Button4 text={loading ? <LoadingSpinner1 size='lds-btn-size' /> : 'Save'}
                        type='submit' form={loading ? null : 'addPersonForm'}
                        />
                    </div>
                </form>
            }
        </div>
    </div>
  )
}

export default AddAllowedPerson