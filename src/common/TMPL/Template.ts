import { ApplicationMeta, ApplicationStateOutput, ApplicationType, UsageType, WalletStateOutput } from '../abstract';
import { getApplicationState, getWalletState } from '../common';

const Template: ApplicationType = class Template {
    static getMeta(): ApplicationMeta {
        // TODO
        return {
            name: 'Template',
            key: 'TMPL',
            type: UsageType.LENDING,
        };
    }

    static fetchStaticApplicationIds(): number[] {
        const applicationIds: number[] = [];
        // TODO
        return applicationIds;
    }

    static fetchDynamicApplicationIds(lastApplicationId: number): number[] {
        const applicationIds: number[] = [];
        // TODO
        return applicationIds;
    }

    static isWalletStateValid(walletState: Record<string, string | number>): boolean {
        // TODO
        return true;
    }

    static isApplicationStateValid(applicationState: Record<string, string | number>): boolean {
        // TODO
        return true;
    }

    static parseWalletState(walletState: Record<string, string | number>): WalletStateOutput {
        const stateOutput: WalletStateOutput = { assetBalances: {} };
        // TODO
        return stateOutput;
    }

    static parseApplicationState(applicationState: Record<string, string | number>): ApplicationStateOutput {
        const stateOutput: ApplicationStateOutput = {
            assetBalances: {},
            timestampFrom: undefined,
            timestampTo: undefined,
            roundFrom: undefined,
            roundTo: undefined,
        };
        // TODO
        return stateOutput;
    }

    static async testApplicationType(): Promise<boolean> {
        // use addresses and application ids that will not break over time
        const testWalletAddress = 'VESTIG3V77NNVBT5SM636UKAZ3M5OQHM76TC5622RQ4Q2XUCYZ5E4ENB3E';
        const testApplicationId = 784136787;
        const walletState = await getWalletState(testWalletAddress, testApplicationId);
        if (Template.isWalletStateValid(walletState)) {
            const values = Template.parseWalletState(walletState);
            // TODO
            // check values, return false if any of them are wrong
        }
        const applicationState = await getApplicationState(testApplicationId);
        if (Template.isApplicationStateValid(applicationState)) {
            const values = Template.parseApplicationState(applicationState);
            // TODO
            // check values, return false if any of them are wrong
        }
        return true;
    }
};

export default Template;
