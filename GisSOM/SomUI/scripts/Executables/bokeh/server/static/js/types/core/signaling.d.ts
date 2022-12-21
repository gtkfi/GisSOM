export declare type Slot<Args, Sender extends object> = (args: Args, sender: Sender) => void;
export declare class Signal<Args, Sender extends object> {
    readonly sender: Sender;
    readonly name: string;
    constructor(sender: Sender, name: string);
    connect(slot: Slot<Args, Sender>, context?: object | null): boolean;
    disconnect(slot: Slot<Args, Sender>, context?: object | null): boolean;
    emit(args: Args): void;
}
export declare class Signal0<Sender extends object> extends Signal<void, Sender> {
    emit(): void;
}
export declare namespace Signal {
    function disconnect_between(sender: object, receiver: object): void;
    function disconnect_sender(sender: object): void;
    function disconnect_receiver(receiver: object, slot?: Slot<any, any>, except_senders?: Set<object>): void;
    function disconnect_all(obj: object): void;
    /** @deprecated */
    const disconnectBetween: typeof disconnect_between;
    /** @deprecated */
    const disconnectSender: typeof disconnect_sender;
    /** @deprecated */
    const disconnectReceiver: typeof disconnect_receiver;
    /** @deprecated */
    const disconnectAll: typeof disconnect_all;
}
export interface ISignalable {
    connect<Args, Sender extends object>(signal: Signal<Args, Sender>, slot: Slot<Args, Sender>): boolean;
    disconnect<Args, Sender extends object>(signal: Signal<Args, Sender>, slot: Slot<Args, Sender>): boolean;
}
export declare function Signalable(): {
    new (): {
        connect<Args, Sender extends object>(signal: Signal<Args, Sender>, slot: Slot<Args, Sender>): boolean;
        disconnect<Args_1, Sender_1 extends object>(signal: Signal<Args_1, Sender_1>, slot: Slot<Args_1, Sender_1>): boolean;
    };
};
//# sourceMappingURL=signaling.d.ts.map