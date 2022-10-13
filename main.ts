import { ApplicationType } from './src/common/abstract';

// imports of Application Types
// import APP_NAME from './src/application_types/APP_KEY/APP_NAME'
import Template from './src/common/TMPL/Template';

// add your application to this list
const APPLICATION_TYPES: Record<string, ApplicationType> = {
    [Template.getMeta()['key']]: Template,
};

const runTestsOfApplications = () => {
    const applicationKeys = Object.keys(APPLICATION_TYPES);
    const applicationCount = applicationKeys.length;
    applicationKeys.forEach((applicationKey, index) => {
        try {
            const ok = APPLICATION_TYPES[applicationKey].testApplicationType();
            if (!ok) {
                throw 'Application test failed.';
            }
            console.info(`[✓] [${index + 1}/${applicationCount}] ${applicationKey}: Test passed.`);
        } catch (e) {
            console.error(`[ ] [${index + 1}/${applicationCount}] ${applicationKey}: Test failed: {e}`);
        }
    });
};

const getApplicationTypeByKey = (applicationKey: string): ApplicationType | undefined => {
    return APPLICATION_TYPES[applicationKey];
};

void runTestsOfApplications();
