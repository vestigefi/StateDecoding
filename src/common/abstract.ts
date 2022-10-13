export enum UsageType {
    // one-sided staking for coins, e.g. VEST -> VEST
    STAKING = 'STKE',
    // one-sided and two-sided staking for coins, e.g. VEST/ALGO LP -> VEST
    FARMING = 'FARM',
    // lending/borrowing protocols
    LENDING = 'LEND',
}

export interface WalletStateOutput {
    assetBalances: Record<number, number>; // { asset_id: asset_balance (no decimals) }, negative balances allowed for ALGO use 0
}

export interface ApplicationStateOutput {
    assetBalances: Record<number, number>; // { asset_id: asset_balance (no decimals) }, negative balances allowed, for ALGO use 0
    timestampFrom?: number; // unix timestamp
    timestampTo?: number; // unix timestamp
    roundFrom?: number;
    roundTo?: number;
}

export interface ApplicationMeta {
    name: string;
    key: string;
    type: UsageType;
}

export interface ApplicationType {
    // Returns application metadata used internally
    getMeta: () => ApplicationMeta;

    // Returns a list of application ids that are not dynamic and not need to be fetched again
    fetchStaticApplicationIds: () => number[] | Promise<number[]>;

    // Return a list of application ids that are dynamic
    // The function should make use of lastApplicationId to only return applications with higher ids
    fetchDynamicApplicationIds: (lastApplicationId: number) => number[] | Promise<number[]>;

    // Return True if passed dict is a valid application state for wallet, else False
    // Check if state contains required for parsing keys and if those keys seem valid
    // If keys are unused in parsing, do not check for their existence
    isWalletStateValid: (walletState: Record<string, string | number>) => boolean | Promise<boolean>;

    // Return True if passed dict is a valid application state, else False
    // Check if state contains required for parsing keys and if those keys seem valid
    // If keys are unused in parsing, do not check for their existence
    isApplicationStateValid: (applicationState: Record<string, string | number>) => boolean | Promise<boolean>;

    // Return parsed local state for given wallet
    parseWalletState: (walletState: Record<string, string | number>) => WalletStateOutput | Promise<WalletStateOutput>;

    // Return parsed global state for given application
    parseApplicationState: (
        applicationState: Record<string, string | number>,
    ) => ApplicationStateOutput | Promise<ApplicationStateOutput>;

    // Dummy function that should call any of the known IDs of this application type using above functions
    // and check if data is valid
    // use get_application_state() from _common
    // Return True if valid, else False
    testApplicationType: () => boolean | Promise<boolean>;
}
