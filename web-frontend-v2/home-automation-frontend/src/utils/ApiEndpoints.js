const baseApiUrl = 'http://127.0.0.1:8000/api/'

const loginUrl = `${baseApiUrl}users/token/`
const loginRefreshUrl = `${baseApiUrl}users/token/refresh/`

const userUrls = {
    createUser:{ "url":`${baseApiUrl}users/list-create/`}
}


const deviceUrls = {
    getAllDevices:{
        url:`${baseApiUrl}devices/list-create/`,
        description:`For retrieving all devices apart of a certain household.
        Add household primary key to end.`,
        methods:['GET', 'POST']
    },
    detailUpdateDevice : {
        url:`${baseApiUrl}devices/detail/`,
        description:`retreive or updates specific device. If requesting method = GET, provide
        db primary key on end. If requesting method = PUT, provide unit id on end.`,
        methods:['GET', 'PUT']
    }, 
    localServerList:{
        url:`${baseApiUrl}devices/local-server/list/`,
        description:`retreive all local servers belonging to a household. Add household id to end`,
        methods:['GET']
    },
    localServerDetail:{
        url:`${baseApiUrl}devices/local-server/detail/`,
        description:`Update or deletes a server`,
        methods:['PUT', 'DELETE']
    }
}

const devicePw = {
    pwDetail :{
        url:`${baseApiUrl}devices/pw/detail/`,
        description:`Delete specific passcode.
        Add code id to end when deleting.`,
        methods:['DELETE']
    },
    pwCreate : {
        url:`${baseApiUrl}devices/pw/create/`,
        description: `Create passcode`,
        methods : ['POST']
    }
}

const alertUrls = {
    getAllAlerts:{
        url:`${baseApiUrl}alerts/list/`,
        description:`For retreiving all alerts belonging to a household.
        Add household key to end.`,
        methods:['GET']
    }
}

const allowed_persons = {
    getAllAllowedPersons:{
        url:`${baseApiUrl}users/allowed-persons/list/`,
        description:`For retreiving all allowed persons belonging to household
        or creating a new allowed person (not for adding household member).
        add household id to end`,
        methods:['GET', 'POST']
    },
    getAllowedPersonDetail:{
        url:`${baseApiUrl}users/allowed-persons/detail/`,
        description:`For retreiving, updating and deleting allowed person.
        add person pk to end`,
        methods:['GET', 'PUT', 'DELETE']
    }
}

export {
    userUrls, baseApiUrl, loginUrl, loginRefreshUrl, deviceUrls, alertUrls, 
    allowed_persons, devicePw
}