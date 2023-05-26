import { ApplicationType } from './src/common/abstract';
import { APPLICATION_TYPES } from './src/application_types/init';

const APPLICATION_TYPES_DICT = APPLICATION_TYPES.reduce((a, v) => ({...a, [v.getMeta()['key']]: v }))

const runTestsOfApplications = () => {
    const applicationKeys = Object.keys(APPLICATION_TYPES_DICT);
    const applicationCount = applicationKeys.length;
    applicationKeys.forEach((applicationKey, index) => {
        try {
            const ok = APPLICATION_TYPES_DICT[applicationKey].testApplicationType();
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
    return APPLICATION_TYPES_DICT[applicationKey];
};

void runTestsOfApplications();
