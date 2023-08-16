import React, { useState, useEffect, useContext, useRef} from "react"
import { useHistory } from "react-router-dom"
import AuthContext from '../../context/AuthContext'
import CustomFetch from "../../utils/CustomFetch"
import { allowed_persons } from "../../utils/ApiEndpoints"
import Error1 from '../loadingAndErrors/Error1'
import LoadingSpinner1 from '../loadingAndErrors/LoadingSpinner1'
import '../../css/general.css'
import '../../css/edit-household.css'
import AllowedPerson from "./AllowedPerson"
import AddBtn from "../buttonsAndInputs/AddBtn"
import { CountRenders } from "../../utils/CountRenders"


const AllowedPersonCardDropdown = () => {
    const {User} = useContext(AuthContext)
    const history = useHistory()
    CountRenders('main card: ')
    const [people, setPeople] = useState(() => null)
    const [loading, setLoading] = useState(() => true)
    const [paginateLoading, setPaginateLoading] = useState(() => false)
    const [error, setError] = useState(() => false)

    const {getAllAllowedPersons} = allowed_persons

    const observer = useRef()

    const handleSetPerson = (data) => {
        const newState = people.results.map(obj => {
            console.log(obj)
            if (obj.id === data.id) {
                console.log(data)
                console.log('yip')
              return data;
            }
      
            return obj;
          });
      
        setPeople((oldArray) => ({results:newState, ...oldArray}));
        console.log(newState)
        console.log(people.results)
    }

    const getPeople = async () => {
        const fetchConfig = {method:'GET'}
        const {response, data} = await CustomFetch(`${getAllAllowedPersons.url}${User.household}/`, fetchConfig)
        if(response.status === 200){
            setPeople(() => data)
            setLoading(() => false)
            return
        }
        setError(() => 'Unable to get data, try again later')
    }

    const handleRemovePerson = (id)  => {
        for(let x = 0; x < people.results.length; x++){
            if(people.results[x].id === id){
                people.results.splice(x, x + 1)
                people.count = people.count - 1
                setPeople(people)
                break
            }
        }
    }

    const handlePaginatePeople = async () => {
        if(!people.next) return
        setPaginateLoading(() => true)
        const fetchConfig = {method:'GET'}
        const {response, data} = await CustomFetch(people.next, fetchConfig)
        if(response.status === 200){
            setPeople(oldArray => ({results:[...oldArray.results, ...data.results], 
                next:data.next, previous:data.previous, count:data.count}))
            setPaginateLoading(() => false)
            return
        }
        setPaginateLoading(() => false)
        setError('Could not get data, try again later')
    }

    const handleTrackPosition = element => {
        if(!people.next) return
        if(observer.current) {observer.current.disconnect()}
        observer.current = new IntersectionObserver(entries => {
          if(entries[0].isIntersecting){
            handlePaginatePeople()
          }
        })
        if(element) {observer.current.observe(element)}
      }

    useEffect(() => {
        getPeople()
    },[])

  return (
    <div className="w-100">
        <div className="w-100 justify-content-center padding-10">
            <AddBtn onClick={() => {history.push('/add-allowed-person')}}/>
        </div>

        {loading && <>
            <div className="w-100 justify-content-center">
                <LoadingSpinner1/>
            </div>
        </>}

        {people && people.count > 0 &&
            people.results.map((person, index) => {
                if(index === people.results.length - 1 && people.next){
                    return <React.Fragment key={index}>
                        <AllowedPerson 
                        person={person} 
                        handleRemovePerson={handleRemovePerson}
                        handleSetPerson={handleSetPerson }
                        />
                        <div ref={handleTrackPosition}></div>
                    </React.Fragment>
                }
                else{
                return <AllowedPerson 
                        key={index}
                        person={person}  
                        handleRemovePerson={handleRemovePerson}
                        handleSetPerson={handleSetPerson }
                        />
                }
            })
        }
       
        {error && <>
            <div className="w-100 justify-content-center">
                <Error1 message={error} />
            </div>
        </>}

        {paginateLoading && <>
            <div className="w-100 justify-content-center">
                <LoadingSpinner1/>
            </div>
        </>}


    </div>
  )
}

export default React.memo(AllowedPersonCardDropdown)