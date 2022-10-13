import axios from 'axios';
export const MAINNET_NODE_API_URL = 'https://mainnet-api.algonode.cloud/';
export const MAINNET_INDEXER_API_URL = 'https://mainnet-idx.algonode.cloud/';

export const getRequest = async (url: string, allowCodes?: number[]): Promise<object> => {
    if (!allowCodes) {
        allowCodes = [];
    }
    const response = await axios.get(url);
    if (response?.statusText !== 'OK' && !allowCodes.includes(response?.status)) {
        throw `Failed GET request: ${url}`;
    }
    return response.data;
};

export const nodeGetRequest = async (endpoint: string, allowCodes?: number[]): Promise<object> => {
    return await getRequest(`${MAINNET_NODE_API_URL}${endpoint}`, allowCodes);
};

export const indexerGetRequest = async (endpoint: string, allowCodes?: number[]): Promise<object> => {
    return await getRequest(`${MAINNET_INDEXER_API_URL}${endpoint}`, allowCodes);
};

const stateEntryToObject = (stateEntry: any): Record<string, string | number> => {
    const stateRecord: Record<string, string | number> = {};
    const valueState = stateEntry?.value || {};
    const valueBytes = stateEntry?.bytes || null;
    stateRecord[stateEntry?.key || 'ERR'] = valueBytes || valueState?.uint;
    return stateRecord;
};

export const getApplicationState = async (applicationId: number): Promise<Record<string, string | number>> => {
    // Returns application state as object (MEANT TO BE USED FOR TESTS ONLY)
    try {
        let state = {};
        const data: any = await indexerGetRequest(`v2/applications/${applicationId}`);
        const application = data.application;
        const params = application.params;
        const localState = params['local-state'];
        const globalState = params['global-state'];
        if (globalState) {
            globalState.forEach((entry: any) => {
                state = { ...state, ...stateEntryToObject(entry) };
            });
        }
        if (localState) {
            localState.forEach((walletState: any) =>
                walletState.forEach((entry: any) => {
                    state = { ...state, ...stateEntryToObject(entry) };
                }),
            );
        }
        return state;
    } catch (e) {
        throw `Couldn't view application state for ID ${applicationId}: ${e}`;
    }
};

export const getWalletState = async (
    address: string,
    applicationId: number,
): Promise<Record<string, string | number>> => {
    // Returns wallet state for application as object (MEANT TO BE USED FOR TESTS ONLY)
    try {
        let state = {};
        const data: any = await indexerGetRequest(`v2/accounts/${address}`);
        const account = data.account;
        const localState = account['apps-local-state'];
        if (localState) {
            localState.forEach((walletState: any) => {
                if (walletState['id'] === applicationId) {
                    (walletState['key-value'] || []).forEach((entry: any) => {
                        state = { ...state, ...stateEntryToObject(entry) };
                    });
                }
            });
        }
        return state;
    } catch (e) {
        throw `Couldn't view application state for ID ${applicationId}: ${e}`;
    }
};

const base64StateToBytes = (keys: string[], state: Promise<Record<string, string | number>>): Uint8Array => {
    const stateBytes = new Uint8Array();
    const stateKeys = Object.keys(state);
    keys.forEach((key) => {
        if (typeof key !== 'string') throw `Key ${key} not found in state.`;
        if (!stateKeys.includes(key)) throw `Key ${key} not found in state.`;
        // TODO
    });
    return stateBytes;
};

export const stateBytesToValues = (ABIString: string, stateBytes: Uint8Array) => {
    // TODO
};
