/*
    1. Сервер должен отправлять все указанные поля.
    Если поле не существует, в таком случае необходимо ввернут null

    2. Обязательность полей отпрляемых клиентом должен определить бэкенд
 */

/**
 * [GET] [OPEN] /open/company
 *
 * Get short info about company
 */
 type GetOpenCompany = {
    res: {
        name: string; // company name
        logo: string; // company logo
    };
};

/**
 * [GET] /company
 *
 * Get a full data about company
 */
type GetCompany = {
    res: {
        id: number; // company id
        name: string; // company name
        logo: string; // company logo
        subdomain: string; // company domain
    };
};

/**
 * [POST] /categories
 *
 * Get list of categories with services list
 */
type GetCategories = {
    req: {
        page: number; // page number
        count: number; // page items count
    };
    res: Array<{
        id: number; // category id
        image: string; // category cover
        name: string; // category name
        description: string; // category description
        services: Array<{
            id: number; // service id
            gender: 1 | 2; // service gender (1 - man, 2 - woman)
            price: number; // service price
            duration: number; // service duration
            break: number; // service break after
            image: string; // service logo
            name: string; // service name
            description: string; // description name
            employees: Array<{
                id: number; // employee id
                name: string; // employee name
                image: string; // employee photo
            }>;
        }>;
    }>;
};

/**
 * [POST] /category/{id}/update
 *
 * Update full category data
 * @param {number} id - category id
 */
type UpdateCategory = {
    req: {
        image: string;
        name: {
            en: string;
            ru: string;
            tr: string;
            de: string;
        };
        description: {
            en: string;
            ru: string;
            tr: string;
            de: string;
        };
    };
};

/**
 * [POST] /category/create
 *
 * Create a new category
 */
type CreateCategory = {
    req: {
        image: string;
        name: {
            en: string;
            ru: string;
            tr: string;
            de: string;
        };
        description: {
            en: string;
            ru: string;
            tr: string;
            de: string;
        };
    };
};

/**
 * [DELETE] /category/{id}/delete
 *
 * Delete a category
 * @param {number} id - category id
 */
type DeleteCategory = {};

/**
 * [POST] /services
 *
 * Get services list
 * Несколькой полей переименовал, брэк убрал так как по бизнесу не нужен (читай чат)
 */
type GetServices = {
    res: Array<{
        id: number; // service id
        gender: 1 | 2; // service gender (1 - man, 2 - woman)
        price: number; // service price
        duration: number; // service duration
        break: number; // service break after
        image: string; // service logo
        name: string; // service name
        description: string; // description name
        employees: Array<{
            id: number; // employee id
            name: string; // employee name
            image: string; // employee photo
        }>;
    }>;
};

/**
 * [POST] /service/{id}/update
 *
 * Update full service data
 * @param {number} id - category id
 * break - убран, категорию если скажешь тоже уберу
 */
type UpdateService = {
    req: {
        gender: 1 | 2; // service gender (1 - man, 2 - woman)
        price: number; // service price
        duration: number; // service duration
        break: number; // service break after
        image: string; // service logo
        name: {
            en: string;
            ru: string;
            tr: string;
            de: string;
        };
        description: {
            en: string;
            ru: string;
            tr: string;
            de: string;
        };
        employees: Array<{
            id: number; // employee id
            name: string; // employee name
            image: string; // employee photo
        }>;
    };
};

/**
 * [POST] /service/create
 *
 * Create a new service
 
 * У меня категория category: 0, не будет вложенного поля так как джанго делает так по дефолту я и не хочу писать костыль лишний
 */
type CreateService = {
    req: {
        gender: 1 | 2; // service gender (1 - man, 2 - woman)
        price: number; // service price
        duration: number; // service duration
        break: number; // service break after
        image: string; // service logo
        name: {
            en: string;
            ru: string;
            tr: string;
            de: string;
        };
        description: {
            en: string;
            ru: string;
            tr: string;
            de: string;
        };
        employees: Array<{
            id: number; // employee id
            name: string; // employee name
            image: string; // employee photo
        }>;
        category: {
            id: number;
        };
    };
};

/**
 * [DELETE] /service/{id}/delete
 *
 * Delete a service
 * @param {number} id - service id
 */
type DeleteService = {};

/**
 * [POST] /clients
 *
 * Get a clients list
 */
type GetClients = {
    req: {
        page: number; // page number
        count: number; // page items count
    };
    res: Array<{
        id: number; // client id
        name: string; // client name
        notes: string; // notes about client
        contacts: {
            phone: string; // client phone
            email: string; // client e-mail
            whatsapp: boolean; // does the client have a WhatsApp
        };
        appointments: {
            count: number; // count of clients appointments
            totalPrice: number; // total price of client appointment
        };
    }>;
};

/**
 * [GET] /client/{id}
 *
 * Get a full client data
 * @param {number} id - client id
 */
type GetClient = {
    res: {
        id: number; // client id
        name: string; // client name
        notes: string; // notes about client
        contacts: {
            phone: string; // client phone
            email: string; // client e-mail
            whatsapp: boolean; // does the client have a WhatsApp
        };
        appointments: {
            count: number; // count of clients appointments
            totalPrice: number; // total price of client appointment
        };
    };
};

/**
 * [POST] /client/{id}/update
 *
 * Update a full client data
 * @param {number} id - client id
 */
type UpdateClient = {
    req: {
        name: string; // client name
        notes: string; // notes about client
        contacts: {
            phone: string; // client phone
            email: string; // client e-mail
            whatsapp: boolean; // does the client have a WhatsApp
        };
    };
};

/**
 * [POST] /client/create
 *
 * Create a new client
 */
type CreateClient = {
    req: {
        name: string; // client name
        notes: string; // notes about client
        contacts: {
            phone: string; // client phone
            email: string; // client e-mail
            whatsapp: boolean; // does the client have a WhatsApp
        };
    };
};

/**
 * [DELETE] /client/{id}/delete
 *
 * Delete a client
 * @param {number} id - client id
 */
type DeleteClient = {};

/**
 * [GET] /employees
 *
 * Get an employees list
 */
type GetEmployees = {
    res: Array<{
        id: number; // employee id
        role: 1 | 2 | 3; // employee role (1 - owner, 2 - admin, 3 - default minimal accesses)
        name: string; // employee name
        email: string; // employee e-mail
        phone: string; // employee phone
        image: string; // employee photo
        status: 1 | 2 | 3; // employee status (1 - working, 2 - not working, 3 - deleted)
        isOwner: boolean;
        services: Array<{
            id: number; // service id
            name: string; // service name
        }>;
    }>;
};

/**
 * [POST] /employee/{id}/update
 *
 * Update an employees data
 * @param {number} id - employee id
 */
type UpdateEmployees = {
    req: {
        role: 2 | 3; // employee role (2 - admin, 3 - default minimal accesses)
        name: string; // employee name
        email: string; // employee e-mail
        phone: string; // employee phone
        image: string; // employee photo
        status: 1 | 2 | 3; // employee status (1 - working, 2 - not working, 3 - deleted)
        services: Array<number>; // array of services id
    };
};

/**
 * [POST] /employee/create
 *
 * Create a new employees
 */
type CreateEmployees = {
    req: {
        role: 2 | 3; // employee role (2 - admin, 3 - default minimal accesses)
        name: string; // employee name
        email: string; // employee e-mail
        phone: string; // employee phone
        image: string; // employee photo
        status: 1 | 2 | 3; // employee status (1 - working, 2 - not working, 3 - deleted)
        services: Array<number>; // array of services id
    };
};

/**
 * [DELETE] /employee/{id}/delete
 *
 * Delete an employees
 * @param {number} id - employee id
 */
type DeleteEmployees = {};

/**
 * [GET] /website
 *
 * Get a full website data
 */
type GetWebsite = {
    res: {
        name: {
            en: string;
            ru: string;
            tr: string;
            de: string;
        };
        description: {
            en: string;
            ru: string;
            tr: string;
            de: string;
        };
        location: {
            // company location (address)
            country: string;
            city: string;
            street: string;
            building: string;

            /*
             * User does create Google Maps Api key in the Google Admin Panel
             * and does upload this key to field from Randevu admin panel
             */
            gmapApiKey: string;
        };
        schedule: {
            /*
             * work-time days of the week (the 1st number - the day of the start,
             * the second number - the day of the end)
             */
            days: [number, number];

            /*
             * work-time intervals of the week (the 1st number - the interval of the start,
             * the second number - the day of the end)
             */
            intervals: [number, number];
        };
        contacts: {
            phone: string;
            facebook: string; // only facebook user id
            instagram: string; // only instagram user id
            whatsapp: string;
        };

        cover: string; // website main image (cover in the first block)
        gallery: Array<string>; // website gallery images
    };
};

/**
 * [POST] /website/update
 *
 * Update a full website data
 */
type UpdateWebsite = {
    req: {
        name: {
            en: string;
            ru: string;
            tr: string;
            de: string;
        };
        description: {
            en: string;
            ru: string;
            tr: string;
            de: string;
        };
        location: {
            // company location (address)
            country: string;
            city: string;
            street: string;
            building: string;

            /*
             * User does create Google Maps Api key in the Google Admin Panel
             * and does upload this key to field from Randevu admin panel
             */
            gmapApiKey: string;
        };
        schedule: {
            /*
             * work-time days of the week (the 1st number - the day of the start,
             * the second number - the day of the end)
             */
            days: [number, number];

            /*
             * work-time intervals of the week (the 1st number - the interval of the start,
             * the second number - the day of the end)
             */
            intervals: [number, number];
        };
        contacts: {
            phone: string;
            facebook: string; // only facebook user id
            instagram: string; // only instagram user id
            whatsapp: string;
        };

        cover: string; // website main image (cover in the first block)
        gallery: Array<string>; // website gallery images
    };
};

/**
 * [GET] /settings
 *
 * Get a full settings data
 */
type GetSettings = {
    res: {
        localization: {
            default: string; // default lang key
            active: Array<'en' | 'ru' | 'tr' | 'de'>; // list of active languages keys
        };
    };
};

/**
 * [POST] /appointments
 *
 * Get an appointments list
 */
type GetAppointments = {
    req: {
        page: number; // page number
        count: number; // page items count
        interval: 1 | 2 | 3; // show items by interval (1 - today, 2 - week, 3 - month)
        status: 0 | 1 | 2 | 3 | 4 | 5; // show items by status (0 - new, 1 - wait, 2 - in progress, 3 - done, 4 - done, 5 - canceled)
    };
    res: {
        id: number;
        index: number; // sequence number
        status: 0 | 1 | 2 | 3 | 4 | 5; // show items by status (0 - new, 1 - wait, 2 - in progress, 3 - done, 4 - done, 5 - canceled)
        date: {
            day: string;
            time: string;
        };
        employee: {
            name: string; // employee name
        };
        client: {
            name: string; // client name
            phone: string;
        };
        service: {
            name: string;
        };
    };
};

/**
 * [GET] /appointment/{id}
 *
 * Get a full appointment data
 * @param {number} id - appointment id
 */
type GetAppointment = {
    res: {
        status: 0 | 1 | 2 | 3 | 4 | 5; // show items by status (0 - new, 1 - wait, 2 - in progress, 3 - done, 4 - done, 5 - canceled)
        date: {
            day: string;
            time: string;
        };
        employee: {
            name: string; // employee name
        };
        client: {
            name: string; // client name
            phone: string;
        };
        service: {
            name: string;
        };
    };
};

/**
 * [POST] /appointment/create
 *
 * Create a new appointment
 */
type CreateAppointment = {
    req: {
        service: {
            id: number;
        };
        employee: {
            id: number;
        };
        client: {
            name: string;
            phone: string;
        };
        date: {
            day: string;
            time: string;
        };
    };
};

/**
 * [POST] /appointment/{id}/update
 *
 * Update an appointment
 * @param {number} id - appointment id
 */
type UpdateAppointment = {
    req: {
        viewed: boolean; // does appointment was viewed
        service: {
            id: number;
        };
        employee: {
            id: number;
        };
        client: {
            name: string;
            phone: string;
        };
        date: {
            day: string;
            time: string;
        };
    };
};

/**
 * [DELETE] /appointment/{id}/cancel
 *
 * Cancel an appointment
 * @param {number} id - appointment id
 */
type UpdateAppointment = {};

/**
 * [POST] /auth/sign-in
 *
 * Sign in to admin-panel
 */
type AuthSignIn = {
    req: {
        login: string; // username or e-mail
        password: string; // user password
    }
    res: {
        jwt: string; // jwt token
    }
};

/**
 * [POST] /auth/logout
 *
 * Logout from admin-panel
 */
type AuthLogout = {};

/**
 * [POST] /auth/recover/get-code
 *
 * Get the auth. code for recover the user password
 */
type AuthRecoverGetCode = {
    req: {
        login: string; // user ONLY e-mail
    }
    res: {
        codeStatus: 'failed' | 'sent';
    }
};

/**
 * [POST] /auth/recover/check-code
 *
 * Check the auth. code for recover the user password
 */
type AuthRecoverCheckCode = {
    req: {
        code: number;
    }
};

/**
 * [POST] /auth/sign-up
 *
 * Sign up to admin-panel
 */
type AuthSignUp = {
    req: {
        email: string;
        sub_domain: string;
        password: string;
    }
    res: {
        operation_id: int
    }
};

/**
 * [GET] /auth/refresh-token
 *
 * Fetch the new JWT token (do refresh every 5 min.)
 */
type AuthRefreshToken = {
    req: {
        fullName: string; // full user`s name
        email: string;
        password: string;
    }
    res: {
        jwt: string;
    }
};

/**
 * [POST] /upload
 *
 * Upload media file (in the future we need upload files with any type that approval)
 */
type Upload = {
    req: {
        image: 'binary';
    }
    res: {
        uuid: string; // The image UUID.
        // Usages of UUID, but not UID or any other ID pattern it is important.
        // We need this UUID for attaching to request to server for uploading image in JSON type form
    }
};

/**
 * [POST] /employee/days
 *
 * Get work days for employee
 */
type GetEmployeeDays = {
    req: {
        id: number; // employee id
        month: number; // from 0 to 11
        year: number; // 2XXX (4 chars)
    }
    res: {
        days: Array<{
          day: number;
          status: boolean;
        }>
    }
};

/**
 * [POST] /employee/times
 *
 * Get work time for employee
 */
type GetEmployeeTimes = {
    req: {
        id: number; // employee id
        date: 'Date'; // dd-mm-yyyy
    }
    res: {
        days: Array<{
          time: number;
          step: number;
          status: boolean;
        }>
    }
};