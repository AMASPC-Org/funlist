
/**
 * Client
**/

import * as runtime from './runtime/library.js';
import $Types = runtime.Types // general types
import $Public = runtime.Types.Public
import $Utils = runtime.Types.Utils
import $Extensions = runtime.Types.Extensions
import $Result = runtime.Types.Result

export type PrismaPromise<T> = $Public.PrismaPromise<T>


/**
 * Model Event
 * 
 */
export type Event = $Result.DefaultSelection<Prisma.$EventPayload>
/**
 * Model User
 * 
 */
export type User = $Result.DefaultSelection<Prisma.$UserPayload>
/**
 * Model Venue
 * 
 */
export type Venue = $Result.DefaultSelection<Prisma.$VenuePayload>
/**
 * Model FunalyticsScore
 * 
 */
export type FunalyticsScore = $Result.DefaultSelection<Prisma.$FunalyticsScorePayload>

/**
 * ##  Prisma Client ʲˢ
 *
 * Type-safe database client for TypeScript & Node.js
 * @example
 * ```
 * const prisma = new PrismaClient()
 * // Fetch zero or more Events
 * const events = await prisma.event.findMany()
 * ```
 *
 *
 * Read more in our [docs](https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client).
 */
export class PrismaClient<
  ClientOptions extends Prisma.PrismaClientOptions = Prisma.PrismaClientOptions,
  const U = 'log' extends keyof ClientOptions ? ClientOptions['log'] extends Array<Prisma.LogLevel | Prisma.LogDefinition> ? Prisma.GetEvents<ClientOptions['log']> : never : never,
  ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs
> {
  [K: symbol]: { types: Prisma.TypeMap<ExtArgs>['other'] }

    /**
   * ##  Prisma Client ʲˢ
   *
   * Type-safe database client for TypeScript & Node.js
   * @example
   * ```
   * const prisma = new PrismaClient()
   * // Fetch zero or more Events
   * const events = await prisma.event.findMany()
   * ```
   *
   *
   * Read more in our [docs](https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client).
   */

  constructor(optionsArg ?: Prisma.Subset<ClientOptions, Prisma.PrismaClientOptions>);
  $on<V extends U>(eventType: V, callback: (event: V extends 'query' ? Prisma.QueryEvent : Prisma.LogEvent) => void): PrismaClient;

  /**
   * Connect with the database
   */
  $connect(): $Utils.JsPromise<void>;

  /**
   * Disconnect from the database
   */
  $disconnect(): $Utils.JsPromise<void>;

/**
   * Executes a prepared raw query and returns the number of affected rows.
   * @example
   * ```
   * const result = await prisma.$executeRaw`UPDATE User SET cool = ${true} WHERE email = ${'user@email.com'};`
   * ```
   *
   * Read more in our [docs](https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client/raw-database-access).
   */
  $executeRaw<T = unknown>(query: TemplateStringsArray | Prisma.Sql, ...values: any[]): Prisma.PrismaPromise<number>;

  /**
   * Executes a raw query and returns the number of affected rows.
   * Susceptible to SQL injections, see documentation.
   * @example
   * ```
   * const result = await prisma.$executeRawUnsafe('UPDATE User SET cool = $1 WHERE email = $2 ;', true, 'user@email.com')
   * ```
   *
   * Read more in our [docs](https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client/raw-database-access).
   */
  $executeRawUnsafe<T = unknown>(query: string, ...values: any[]): Prisma.PrismaPromise<number>;

  /**
   * Performs a prepared raw query and returns the `SELECT` data.
   * @example
   * ```
   * const result = await prisma.$queryRaw`SELECT * FROM User WHERE id = ${1} OR email = ${'user@email.com'};`
   * ```
   *
   * Read more in our [docs](https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client/raw-database-access).
   */
  $queryRaw<T = unknown>(query: TemplateStringsArray | Prisma.Sql, ...values: any[]): Prisma.PrismaPromise<T>;

  /**
   * Performs a raw query and returns the `SELECT` data.
   * Susceptible to SQL injections, see documentation.
   * @example
   * ```
   * const result = await prisma.$queryRawUnsafe('SELECT * FROM User WHERE id = $1 OR email = $2;', 1, 'user@email.com')
   * ```
   *
   * Read more in our [docs](https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client/raw-database-access).
   */
  $queryRawUnsafe<T = unknown>(query: string, ...values: any[]): Prisma.PrismaPromise<T>;


  /**
   * Allows the running of a sequence of read/write operations that are guaranteed to either succeed or fail as a whole.
   * @example
   * ```
   * const [george, bob, alice] = await prisma.$transaction([
   *   prisma.user.create({ data: { name: 'George' } }),
   *   prisma.user.create({ data: { name: 'Bob' } }),
   *   prisma.user.create({ data: { name: 'Alice' } }),
   * ])
   * ```
   * 
   * Read more in our [docs](https://www.prisma.io/docs/concepts/components/prisma-client/transactions).
   */
  $transaction<P extends Prisma.PrismaPromise<any>[]>(arg: [...P], options?: { isolationLevel?: Prisma.TransactionIsolationLevel }): $Utils.JsPromise<runtime.Types.Utils.UnwrapTuple<P>>

  $transaction<R>(fn: (prisma: Omit<PrismaClient, runtime.ITXClientDenyList>) => $Utils.JsPromise<R>, options?: { maxWait?: number, timeout?: number, isolationLevel?: Prisma.TransactionIsolationLevel }): $Utils.JsPromise<R>


  $extends: $Extensions.ExtendsHook<"extends", Prisma.TypeMapCb<ClientOptions>, ExtArgs, $Utils.Call<Prisma.TypeMapCb<ClientOptions>, {
    extArgs: ExtArgs
  }>>

      /**
   * `prisma.event`: Exposes CRUD operations for the **Event** model.
    * Example usage:
    * ```ts
    * // Fetch zero or more Events
    * const events = await prisma.event.findMany()
    * ```
    */
  get event(): Prisma.EventDelegate<ExtArgs, ClientOptions>;

  /**
   * `prisma.user`: Exposes CRUD operations for the **User** model.
    * Example usage:
    * ```ts
    * // Fetch zero or more Users
    * const users = await prisma.user.findMany()
    * ```
    */
  get user(): Prisma.UserDelegate<ExtArgs, ClientOptions>;

  /**
   * `prisma.venue`: Exposes CRUD operations for the **Venue** model.
    * Example usage:
    * ```ts
    * // Fetch zero or more Venues
    * const venues = await prisma.venue.findMany()
    * ```
    */
  get venue(): Prisma.VenueDelegate<ExtArgs, ClientOptions>;

  /**
   * `prisma.funalyticsScore`: Exposes CRUD operations for the **FunalyticsScore** model.
    * Example usage:
    * ```ts
    * // Fetch zero or more FunalyticsScores
    * const funalyticsScores = await prisma.funalyticsScore.findMany()
    * ```
    */
  get funalyticsScore(): Prisma.FunalyticsScoreDelegate<ExtArgs, ClientOptions>;
}

export namespace Prisma {
  export import DMMF = runtime.DMMF

  export type PrismaPromise<T> = $Public.PrismaPromise<T>

  /**
   * Validator
   */
  export import validator = runtime.Public.validator

  /**
   * Prisma Errors
   */
  export import PrismaClientKnownRequestError = runtime.PrismaClientKnownRequestError
  export import PrismaClientUnknownRequestError = runtime.PrismaClientUnknownRequestError
  export import PrismaClientRustPanicError = runtime.PrismaClientRustPanicError
  export import PrismaClientInitializationError = runtime.PrismaClientInitializationError
  export import PrismaClientValidationError = runtime.PrismaClientValidationError

  /**
   * Re-export of sql-template-tag
   */
  export import sql = runtime.sqltag
  export import empty = runtime.empty
  export import join = runtime.join
  export import raw = runtime.raw
  export import Sql = runtime.Sql



  /**
   * Decimal.js
   */
  export import Decimal = runtime.Decimal

  export type DecimalJsLike = runtime.DecimalJsLike

  /**
   * Metrics
   */
  export type Metrics = runtime.Metrics
  export type Metric<T> = runtime.Metric<T>
  export type MetricHistogram = runtime.MetricHistogram
  export type MetricHistogramBucket = runtime.MetricHistogramBucket

  /**
  * Extensions
  */
  export import Extension = $Extensions.UserArgs
  export import getExtensionContext = runtime.Extensions.getExtensionContext
  export import Args = $Public.Args
  export import Payload = $Public.Payload
  export import Result = $Public.Result
  export import Exact = $Public.Exact

  /**
   * Prisma Client JS version: 6.16.1
   * Query Engine version: 1c57fdcd7e44b29b9313256c76699e91c3ac3c43
   */
  export type PrismaVersion = {
    client: string
  }

  export const prismaVersion: PrismaVersion

  /**
   * Utility Types
   */


  export import JsonObject = runtime.JsonObject
  export import JsonArray = runtime.JsonArray
  export import JsonValue = runtime.JsonValue
  export import InputJsonObject = runtime.InputJsonObject
  export import InputJsonArray = runtime.InputJsonArray
  export import InputJsonValue = runtime.InputJsonValue

  /**
   * Types of the values used to represent different kinds of `null` values when working with JSON fields.
   *
   * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-on-a-json-field
   */
  namespace NullTypes {
    /**
    * Type of `Prisma.DbNull`.
    *
    * You cannot use other instances of this class. Please use the `Prisma.DbNull` value.
    *
    * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-on-a-json-field
    */
    class DbNull {
      private DbNull: never
      private constructor()
    }

    /**
    * Type of `Prisma.JsonNull`.
    *
    * You cannot use other instances of this class. Please use the `Prisma.JsonNull` value.
    *
    * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-on-a-json-field
    */
    class JsonNull {
      private JsonNull: never
      private constructor()
    }

    /**
    * Type of `Prisma.AnyNull`.
    *
    * You cannot use other instances of this class. Please use the `Prisma.AnyNull` value.
    *
    * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-on-a-json-field
    */
    class AnyNull {
      private AnyNull: never
      private constructor()
    }
  }

  /**
   * Helper for filtering JSON entries that have `null` on the database (empty on the db)
   *
   * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-on-a-json-field
   */
  export const DbNull: NullTypes.DbNull

  /**
   * Helper for filtering JSON entries that have JSON `null` values (not empty on the db)
   *
   * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-on-a-json-field
   */
  export const JsonNull: NullTypes.JsonNull

  /**
   * Helper for filtering JSON entries that are `Prisma.DbNull` or `Prisma.JsonNull`
   *
   * @see https://www.prisma.io/docs/concepts/components/prisma-client/working-with-fields/working-with-json-fields#filtering-on-a-json-field
   */
  export const AnyNull: NullTypes.AnyNull

  type SelectAndInclude = {
    select: any
    include: any
  }

  type SelectAndOmit = {
    select: any
    omit: any
  }

  /**
   * Get the type of the value, that the Promise holds.
   */
  export type PromiseType<T extends PromiseLike<any>> = T extends PromiseLike<infer U> ? U : T;

  /**
   * Get the return type of a function which returns a Promise.
   */
  export type PromiseReturnType<T extends (...args: any) => $Utils.JsPromise<any>> = PromiseType<ReturnType<T>>

  /**
   * From T, pick a set of properties whose keys are in the union K
   */
  type Prisma__Pick<T, K extends keyof T> = {
      [P in K]: T[P];
  };


  export type Enumerable<T> = T | Array<T>;

  export type RequiredKeys<T> = {
    [K in keyof T]-?: {} extends Prisma__Pick<T, K> ? never : K
  }[keyof T]

  export type TruthyKeys<T> = keyof {
    [K in keyof T as T[K] extends false | undefined | null ? never : K]: K
  }

  export type TrueKeys<T> = TruthyKeys<Prisma__Pick<T, RequiredKeys<T>>>

  /**
   * Subset
   * @desc From `T` pick properties that exist in `U`. Simple version of Intersection
   */
  export type Subset<T, U> = {
    [key in keyof T]: key extends keyof U ? T[key] : never;
  };

  /**
   * SelectSubset
   * @desc From `T` pick properties that exist in `U`. Simple version of Intersection.
   * Additionally, it validates, if both select and include are present. If the case, it errors.
   */
  export type SelectSubset<T, U> = {
    [key in keyof T]: key extends keyof U ? T[key] : never
  } &
    (T extends SelectAndInclude
      ? 'Please either choose `select` or `include`.'
      : T extends SelectAndOmit
        ? 'Please either choose `select` or `omit`.'
        : {})

  /**
   * Subset + Intersection
   * @desc From `T` pick properties that exist in `U` and intersect `K`
   */
  export type SubsetIntersection<T, U, K> = {
    [key in keyof T]: key extends keyof U ? T[key] : never
  } &
    K

  type Without<T, U> = { [P in Exclude<keyof T, keyof U>]?: never };

  /**
   * XOR is needed to have a real mutually exclusive union type
   * https://stackoverflow.com/questions/42123407/does-typescript-support-mutually-exclusive-types
   */
  type XOR<T, U> =
    T extends object ?
    U extends object ?
      (Without<T, U> & U) | (Without<U, T> & T)
    : U : T


  /**
   * Is T a Record?
   */
  type IsObject<T extends any> = T extends Array<any>
  ? False
  : T extends Date
  ? False
  : T extends Uint8Array
  ? False
  : T extends BigInt
  ? False
  : T extends object
  ? True
  : False


  /**
   * If it's T[], return T
   */
  export type UnEnumerate<T extends unknown> = T extends Array<infer U> ? U : T

  /**
   * From ts-toolbelt
   */

  type __Either<O extends object, K extends Key> = Omit<O, K> &
    {
      // Merge all but K
      [P in K]: Prisma__Pick<O, P & keyof O> // With K possibilities
    }[K]

  type EitherStrict<O extends object, K extends Key> = Strict<__Either<O, K>>

  type EitherLoose<O extends object, K extends Key> = ComputeRaw<__Either<O, K>>

  type _Either<
    O extends object,
    K extends Key,
    strict extends Boolean
  > = {
    1: EitherStrict<O, K>
    0: EitherLoose<O, K>
  }[strict]

  type Either<
    O extends object,
    K extends Key,
    strict extends Boolean = 1
  > = O extends unknown ? _Either<O, K, strict> : never

  export type Union = any

  type PatchUndefined<O extends object, O1 extends object> = {
    [K in keyof O]: O[K] extends undefined ? At<O1, K> : O[K]
  } & {}

  /** Helper Types for "Merge" **/
  export type IntersectOf<U extends Union> = (
    U extends unknown ? (k: U) => void : never
  ) extends (k: infer I) => void
    ? I
    : never

  export type Overwrite<O extends object, O1 extends object> = {
      [K in keyof O]: K extends keyof O1 ? O1[K] : O[K];
  } & {};

  type _Merge<U extends object> = IntersectOf<Overwrite<U, {
      [K in keyof U]-?: At<U, K>;
  }>>;

  type Key = string | number | symbol;
  type AtBasic<O extends object, K extends Key> = K extends keyof O ? O[K] : never;
  type AtStrict<O extends object, K extends Key> = O[K & keyof O];
  type AtLoose<O extends object, K extends Key> = O extends unknown ? AtStrict<O, K> : never;
  export type At<O extends object, K extends Key, strict extends Boolean = 1> = {
      1: AtStrict<O, K>;
      0: AtLoose<O, K>;
  }[strict];

  export type ComputeRaw<A extends any> = A extends Function ? A : {
    [K in keyof A]: A[K];
  } & {};

  export type OptionalFlat<O> = {
    [K in keyof O]?: O[K];
  } & {};

  type _Record<K extends keyof any, T> = {
    [P in K]: T;
  };

  // cause typescript not to expand types and preserve names
  type NoExpand<T> = T extends unknown ? T : never;

  // this type assumes the passed object is entirely optional
  type AtLeast<O extends object, K extends string> = NoExpand<
    O extends unknown
    ? | (K extends keyof O ? { [P in K]: O[P] } & O : O)
      | {[P in keyof O as P extends K ? P : never]-?: O[P]} & O
    : never>;

  type _Strict<U, _U = U> = U extends unknown ? U & OptionalFlat<_Record<Exclude<Keys<_U>, keyof U>, never>> : never;

  export type Strict<U extends object> = ComputeRaw<_Strict<U>>;
  /** End Helper Types for "Merge" **/

  export type Merge<U extends object> = ComputeRaw<_Merge<Strict<U>>>;

  /**
  A [[Boolean]]
  */
  export type Boolean = True | False

  // /**
  // 1
  // */
  export type True = 1

  /**
  0
  */
  export type False = 0

  export type Not<B extends Boolean> = {
    0: 1
    1: 0
  }[B]

  export type Extends<A1 extends any, A2 extends any> = [A1] extends [never]
    ? 0 // anything `never` is false
    : A1 extends A2
    ? 1
    : 0

  export type Has<U extends Union, U1 extends Union> = Not<
    Extends<Exclude<U1, U>, U1>
  >

  export type Or<B1 extends Boolean, B2 extends Boolean> = {
    0: {
      0: 0
      1: 1
    }
    1: {
      0: 1
      1: 1
    }
  }[B1][B2]

  export type Keys<U extends Union> = U extends unknown ? keyof U : never

  type Cast<A, B> = A extends B ? A : B;

  export const type: unique symbol;



  /**
   * Used by group by
   */

  export type GetScalarType<T, O> = O extends object ? {
    [P in keyof T]: P extends keyof O
      ? O[P]
      : never
  } : never

  type FieldPaths<
    T,
    U = Omit<T, '_avg' | '_sum' | '_count' | '_min' | '_max'>
  > = IsObject<T> extends True ? U : T

  type GetHavingFields<T> = {
    [K in keyof T]: Or<
      Or<Extends<'OR', K>, Extends<'AND', K>>,
      Extends<'NOT', K>
    > extends True
      ? // infer is only needed to not hit TS limit
        // based on the brilliant idea of Pierre-Antoine Mills
        // https://github.com/microsoft/TypeScript/issues/30188#issuecomment-478938437
        T[K] extends infer TK
        ? GetHavingFields<UnEnumerate<TK> extends object ? Merge<UnEnumerate<TK>> : never>
        : never
      : {} extends FieldPaths<T[K]>
      ? never
      : K
  }[keyof T]

  /**
   * Convert tuple to union
   */
  type _TupleToUnion<T> = T extends (infer E)[] ? E : never
  type TupleToUnion<K extends readonly any[]> = _TupleToUnion<K>
  type MaybeTupleToUnion<T> = T extends any[] ? TupleToUnion<T> : T

  /**
   * Like `Pick`, but additionally can also accept an array of keys
   */
  type PickEnumerable<T, K extends Enumerable<keyof T> | keyof T> = Prisma__Pick<T, MaybeTupleToUnion<K>>

  /**
   * Exclude all keys with underscores
   */
  type ExcludeUnderscoreKeys<T extends string> = T extends `_${string}` ? never : T


  export type FieldRef<Model, FieldType> = runtime.FieldRef<Model, FieldType>

  type FieldRefInputType<Model, FieldType> = Model extends never ? never : FieldRef<Model, FieldType>


  export const ModelName: {
    Event: 'Event',
    User: 'User',
    Venue: 'Venue',
    FunalyticsScore: 'FunalyticsScore'
  };

  export type ModelName = (typeof ModelName)[keyof typeof ModelName]


  export type Datasources = {
    db?: Datasource
  }

  interface TypeMapCb<ClientOptions = {}> extends $Utils.Fn<{extArgs: $Extensions.InternalArgs }, $Utils.Record<string, any>> {
    returns: Prisma.TypeMap<this['params']['extArgs'], ClientOptions extends { omit: infer OmitOptions } ? OmitOptions : {}>
  }

  export type TypeMap<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs, GlobalOmitOptions = {}> = {
    globalOmitOptions: {
      omit: GlobalOmitOptions
    }
    meta: {
      modelProps: "event" | "user" | "venue" | "funalyticsScore"
      txIsolationLevel: Prisma.TransactionIsolationLevel
    }
    model: {
      Event: {
        payload: Prisma.$EventPayload<ExtArgs>
        fields: Prisma.EventFieldRefs
        operations: {
          findUnique: {
            args: Prisma.EventFindUniqueArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$EventPayload> | null
          }
          findUniqueOrThrow: {
            args: Prisma.EventFindUniqueOrThrowArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$EventPayload>
          }
          findFirst: {
            args: Prisma.EventFindFirstArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$EventPayload> | null
          }
          findFirstOrThrow: {
            args: Prisma.EventFindFirstOrThrowArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$EventPayload>
          }
          findMany: {
            args: Prisma.EventFindManyArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$EventPayload>[]
          }
          create: {
            args: Prisma.EventCreateArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$EventPayload>
          }
          createMany: {
            args: Prisma.EventCreateManyArgs<ExtArgs>
            result: BatchPayload
          }
          createManyAndReturn: {
            args: Prisma.EventCreateManyAndReturnArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$EventPayload>[]
          }
          delete: {
            args: Prisma.EventDeleteArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$EventPayload>
          }
          update: {
            args: Prisma.EventUpdateArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$EventPayload>
          }
          deleteMany: {
            args: Prisma.EventDeleteManyArgs<ExtArgs>
            result: BatchPayload
          }
          updateMany: {
            args: Prisma.EventUpdateManyArgs<ExtArgs>
            result: BatchPayload
          }
          updateManyAndReturn: {
            args: Prisma.EventUpdateManyAndReturnArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$EventPayload>[]
          }
          upsert: {
            args: Prisma.EventUpsertArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$EventPayload>
          }
          aggregate: {
            args: Prisma.EventAggregateArgs<ExtArgs>
            result: $Utils.Optional<AggregateEvent>
          }
          groupBy: {
            args: Prisma.EventGroupByArgs<ExtArgs>
            result: $Utils.Optional<EventGroupByOutputType>[]
          }
          count: {
            args: Prisma.EventCountArgs<ExtArgs>
            result: $Utils.Optional<EventCountAggregateOutputType> | number
          }
        }
      }
      User: {
        payload: Prisma.$UserPayload<ExtArgs>
        fields: Prisma.UserFieldRefs
        operations: {
          findUnique: {
            args: Prisma.UserFindUniqueArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$UserPayload> | null
          }
          findUniqueOrThrow: {
            args: Prisma.UserFindUniqueOrThrowArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$UserPayload>
          }
          findFirst: {
            args: Prisma.UserFindFirstArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$UserPayload> | null
          }
          findFirstOrThrow: {
            args: Prisma.UserFindFirstOrThrowArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$UserPayload>
          }
          findMany: {
            args: Prisma.UserFindManyArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$UserPayload>[]
          }
          create: {
            args: Prisma.UserCreateArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$UserPayload>
          }
          createMany: {
            args: Prisma.UserCreateManyArgs<ExtArgs>
            result: BatchPayload
          }
          createManyAndReturn: {
            args: Prisma.UserCreateManyAndReturnArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$UserPayload>[]
          }
          delete: {
            args: Prisma.UserDeleteArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$UserPayload>
          }
          update: {
            args: Prisma.UserUpdateArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$UserPayload>
          }
          deleteMany: {
            args: Prisma.UserDeleteManyArgs<ExtArgs>
            result: BatchPayload
          }
          updateMany: {
            args: Prisma.UserUpdateManyArgs<ExtArgs>
            result: BatchPayload
          }
          updateManyAndReturn: {
            args: Prisma.UserUpdateManyAndReturnArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$UserPayload>[]
          }
          upsert: {
            args: Prisma.UserUpsertArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$UserPayload>
          }
          aggregate: {
            args: Prisma.UserAggregateArgs<ExtArgs>
            result: $Utils.Optional<AggregateUser>
          }
          groupBy: {
            args: Prisma.UserGroupByArgs<ExtArgs>
            result: $Utils.Optional<UserGroupByOutputType>[]
          }
          count: {
            args: Prisma.UserCountArgs<ExtArgs>
            result: $Utils.Optional<UserCountAggregateOutputType> | number
          }
        }
      }
      Venue: {
        payload: Prisma.$VenuePayload<ExtArgs>
        fields: Prisma.VenueFieldRefs
        operations: {
          findUnique: {
            args: Prisma.VenueFindUniqueArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$VenuePayload> | null
          }
          findUniqueOrThrow: {
            args: Prisma.VenueFindUniqueOrThrowArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$VenuePayload>
          }
          findFirst: {
            args: Prisma.VenueFindFirstArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$VenuePayload> | null
          }
          findFirstOrThrow: {
            args: Prisma.VenueFindFirstOrThrowArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$VenuePayload>
          }
          findMany: {
            args: Prisma.VenueFindManyArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$VenuePayload>[]
          }
          create: {
            args: Prisma.VenueCreateArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$VenuePayload>
          }
          createMany: {
            args: Prisma.VenueCreateManyArgs<ExtArgs>
            result: BatchPayload
          }
          createManyAndReturn: {
            args: Prisma.VenueCreateManyAndReturnArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$VenuePayload>[]
          }
          delete: {
            args: Prisma.VenueDeleteArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$VenuePayload>
          }
          update: {
            args: Prisma.VenueUpdateArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$VenuePayload>
          }
          deleteMany: {
            args: Prisma.VenueDeleteManyArgs<ExtArgs>
            result: BatchPayload
          }
          updateMany: {
            args: Prisma.VenueUpdateManyArgs<ExtArgs>
            result: BatchPayload
          }
          updateManyAndReturn: {
            args: Prisma.VenueUpdateManyAndReturnArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$VenuePayload>[]
          }
          upsert: {
            args: Prisma.VenueUpsertArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$VenuePayload>
          }
          aggregate: {
            args: Prisma.VenueAggregateArgs<ExtArgs>
            result: $Utils.Optional<AggregateVenue>
          }
          groupBy: {
            args: Prisma.VenueGroupByArgs<ExtArgs>
            result: $Utils.Optional<VenueGroupByOutputType>[]
          }
          count: {
            args: Prisma.VenueCountArgs<ExtArgs>
            result: $Utils.Optional<VenueCountAggregateOutputType> | number
          }
        }
      }
      FunalyticsScore: {
        payload: Prisma.$FunalyticsScorePayload<ExtArgs>
        fields: Prisma.FunalyticsScoreFieldRefs
        operations: {
          findUnique: {
            args: Prisma.FunalyticsScoreFindUniqueArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$FunalyticsScorePayload> | null
          }
          findUniqueOrThrow: {
            args: Prisma.FunalyticsScoreFindUniqueOrThrowArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$FunalyticsScorePayload>
          }
          findFirst: {
            args: Prisma.FunalyticsScoreFindFirstArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$FunalyticsScorePayload> | null
          }
          findFirstOrThrow: {
            args: Prisma.FunalyticsScoreFindFirstOrThrowArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$FunalyticsScorePayload>
          }
          findMany: {
            args: Prisma.FunalyticsScoreFindManyArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$FunalyticsScorePayload>[]
          }
          create: {
            args: Prisma.FunalyticsScoreCreateArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$FunalyticsScorePayload>
          }
          createMany: {
            args: Prisma.FunalyticsScoreCreateManyArgs<ExtArgs>
            result: BatchPayload
          }
          createManyAndReturn: {
            args: Prisma.FunalyticsScoreCreateManyAndReturnArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$FunalyticsScorePayload>[]
          }
          delete: {
            args: Prisma.FunalyticsScoreDeleteArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$FunalyticsScorePayload>
          }
          update: {
            args: Prisma.FunalyticsScoreUpdateArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$FunalyticsScorePayload>
          }
          deleteMany: {
            args: Prisma.FunalyticsScoreDeleteManyArgs<ExtArgs>
            result: BatchPayload
          }
          updateMany: {
            args: Prisma.FunalyticsScoreUpdateManyArgs<ExtArgs>
            result: BatchPayload
          }
          updateManyAndReturn: {
            args: Prisma.FunalyticsScoreUpdateManyAndReturnArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$FunalyticsScorePayload>[]
          }
          upsert: {
            args: Prisma.FunalyticsScoreUpsertArgs<ExtArgs>
            result: $Utils.PayloadToResult<Prisma.$FunalyticsScorePayload>
          }
          aggregate: {
            args: Prisma.FunalyticsScoreAggregateArgs<ExtArgs>
            result: $Utils.Optional<AggregateFunalyticsScore>
          }
          groupBy: {
            args: Prisma.FunalyticsScoreGroupByArgs<ExtArgs>
            result: $Utils.Optional<FunalyticsScoreGroupByOutputType>[]
          }
          count: {
            args: Prisma.FunalyticsScoreCountArgs<ExtArgs>
            result: $Utils.Optional<FunalyticsScoreCountAggregateOutputType> | number
          }
        }
      }
    }
  } & {
    other: {
      payload: any
      operations: {
        $executeRaw: {
          args: [query: TemplateStringsArray | Prisma.Sql, ...values: any[]],
          result: any
        }
        $executeRawUnsafe: {
          args: [query: string, ...values: any[]],
          result: any
        }
        $queryRaw: {
          args: [query: TemplateStringsArray | Prisma.Sql, ...values: any[]],
          result: any
        }
        $queryRawUnsafe: {
          args: [query: string, ...values: any[]],
          result: any
        }
      }
    }
  }
  export const defineExtension: $Extensions.ExtendsHook<"define", Prisma.TypeMapCb, $Extensions.DefaultArgs>
  export type DefaultPrismaClient = PrismaClient
  export type ErrorFormat = 'pretty' | 'colorless' | 'minimal'
  export interface PrismaClientOptions {
    /**
     * Overwrites the datasource url from your schema.prisma file
     */
    datasources?: Datasources
    /**
     * Overwrites the datasource url from your schema.prisma file
     */
    datasourceUrl?: string
    /**
     * @default "colorless"
     */
    errorFormat?: ErrorFormat
    /**
     * @example
     * ```
     * // Shorthand for `emit: 'stdout'`
     * log: ['query', 'info', 'warn', 'error']
     * 
     * // Emit as events only
     * log: [
     *   { emit: 'event', level: 'query' },
     *   { emit: 'event', level: 'info' },
     *   { emit: 'event', level: 'warn' }
     *   { emit: 'event', level: 'error' }
     * ]
     * 
     * / Emit as events and log to stdout
     * og: [
     *  { emit: 'stdout', level: 'query' },
     *  { emit: 'stdout', level: 'info' },
     *  { emit: 'stdout', level: 'warn' }
     *  { emit: 'stdout', level: 'error' }
     * 
     * ```
     * Read more in our [docs](https://www.prisma.io/docs/reference/tools-and-interfaces/prisma-client/logging#the-log-option).
     */
    log?: (LogLevel | LogDefinition)[]
    /**
     * The default values for transactionOptions
     * maxWait ?= 2000
     * timeout ?= 5000
     */
    transactionOptions?: {
      maxWait?: number
      timeout?: number
      isolationLevel?: Prisma.TransactionIsolationLevel
    }
    /**
     * Instance of a Driver Adapter, e.g., like one provided by `@prisma/adapter-planetscale`
     */
    adapter?: runtime.SqlDriverAdapterFactory | null
    /**
     * Global configuration for omitting model fields by default.
     * 
     * @example
     * ```
     * const prisma = new PrismaClient({
     *   omit: {
     *     user: {
     *       password: true
     *     }
     *   }
     * })
     * ```
     */
    omit?: Prisma.GlobalOmitConfig
  }
  export type GlobalOmitConfig = {
    event?: EventOmit
    user?: UserOmit
    venue?: VenueOmit
    funalyticsScore?: FunalyticsScoreOmit
  }

  /* Types for Logging */
  export type LogLevel = 'info' | 'query' | 'warn' | 'error'
  export type LogDefinition = {
    level: LogLevel
    emit: 'stdout' | 'event'
  }

  export type CheckIsLogLevel<T> = T extends LogLevel ? T : never;

  export type GetLogType<T> = CheckIsLogLevel<
    T extends LogDefinition ? T['level'] : T
  >;

  export type GetEvents<T extends any[]> = T extends Array<LogLevel | LogDefinition>
    ? GetLogType<T[number]>
    : never;

  export type QueryEvent = {
    timestamp: Date
    query: string
    params: string
    duration: number
    target: string
  }

  export type LogEvent = {
    timestamp: Date
    message: string
    target: string
  }
  /* End Types for Logging */


  export type PrismaAction =
    | 'findUnique'
    | 'findUniqueOrThrow'
    | 'findMany'
    | 'findFirst'
    | 'findFirstOrThrow'
    | 'create'
    | 'createMany'
    | 'createManyAndReturn'
    | 'update'
    | 'updateMany'
    | 'updateManyAndReturn'
    | 'upsert'
    | 'delete'
    | 'deleteMany'
    | 'executeRaw'
    | 'queryRaw'
    | 'aggregate'
    | 'count'
    | 'runCommandRaw'
    | 'findRaw'
    | 'groupBy'

  // tested in getLogLevel.test.ts
  export function getLogLevel(log: Array<LogLevel | LogDefinition>): LogLevel | undefined;

  /**
   * `PrismaClient` proxy available in interactive transactions.
   */
  export type TransactionClient = Omit<Prisma.DefaultPrismaClient, runtime.ITXClientDenyList>

  export type Datasource = {
    url?: string
  }

  /**
   * Count Types
   */


  /**
   * Count Type EventCountOutputType
   */

  export type EventCountOutputType = {
    funalytics: number
  }

  export type EventCountOutputTypeSelect<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    funalytics?: boolean | EventCountOutputTypeCountFunalyticsArgs
  }

  // Custom InputTypes
  /**
   * EventCountOutputType without action
   */
  export type EventCountOutputTypeDefaultArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the EventCountOutputType
     */
    select?: EventCountOutputTypeSelect<ExtArgs> | null
  }

  /**
   * EventCountOutputType without action
   */
  export type EventCountOutputTypeCountFunalyticsArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    where?: FunalyticsScoreWhereInput
  }


  /**
   * Count Type UserCountOutputType
   */

  export type UserCountOutputType = {
    events: number
  }

  export type UserCountOutputTypeSelect<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    events?: boolean | UserCountOutputTypeCountEventsArgs
  }

  // Custom InputTypes
  /**
   * UserCountOutputType without action
   */
  export type UserCountOutputTypeDefaultArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the UserCountOutputType
     */
    select?: UserCountOutputTypeSelect<ExtArgs> | null
  }

  /**
   * UserCountOutputType without action
   */
  export type UserCountOutputTypeCountEventsArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    where?: EventWhereInput
  }


  /**
   * Count Type VenueCountOutputType
   */

  export type VenueCountOutputType = {
    events: number
  }

  export type VenueCountOutputTypeSelect<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    events?: boolean | VenueCountOutputTypeCountEventsArgs
  }

  // Custom InputTypes
  /**
   * VenueCountOutputType without action
   */
  export type VenueCountOutputTypeDefaultArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the VenueCountOutputType
     */
    select?: VenueCountOutputTypeSelect<ExtArgs> | null
  }

  /**
   * VenueCountOutputType without action
   */
  export type VenueCountOutputTypeCountEventsArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    where?: EventWhereInput
  }


  /**
   * Models
   */

  /**
   * Model Event
   */

  export type AggregateEvent = {
    _count: EventCountAggregateOutputType | null
    _avg: EventAvgAggregateOutputType | null
    _sum: EventSumAggregateOutputType | null
    _min: EventMinAggregateOutputType | null
    _max: EventMaxAggregateOutputType | null
  }

  export type EventAvgAggregateOutputType = {
    id: number | null
    latitude: number | null
    longitude: number | null
    organizerId: number | null
    venueId: number | null
  }

  export type EventSumAggregateOutputType = {
    id: number | null
    latitude: number | null
    longitude: number | null
    organizerId: number | null
    venueId: number | null
  }

  export type EventMinAggregateOutputType = {
    id: number | null
    title: string | null
    description: string | null
    startTime: Date | null
    endTime: Date | null
    location: string | null
    city: string | null
    state: string | null
    zipCode: string | null
    latitude: number | null
    longitude: number | null
    category: string | null
    organizerId: number | null
    venueId: number | null
    status: string | null
    created_at: Date | null
    updated_at: Date | null
  }

  export type EventMaxAggregateOutputType = {
    id: number | null
    title: string | null
    description: string | null
    startTime: Date | null
    endTime: Date | null
    location: string | null
    city: string | null
    state: string | null
    zipCode: string | null
    latitude: number | null
    longitude: number | null
    category: string | null
    organizerId: number | null
    venueId: number | null
    status: string | null
    created_at: Date | null
    updated_at: Date | null
  }

  export type EventCountAggregateOutputType = {
    id: number
    title: number
    description: number
    startTime: number
    endTime: number
    location: number
    city: number
    state: number
    zipCode: number
    latitude: number
    longitude: number
    category: number
    organizerId: number
    venueId: number
    status: number
    created_at: number
    updated_at: number
    _all: number
  }


  export type EventAvgAggregateInputType = {
    id?: true
    latitude?: true
    longitude?: true
    organizerId?: true
    venueId?: true
  }

  export type EventSumAggregateInputType = {
    id?: true
    latitude?: true
    longitude?: true
    organizerId?: true
    venueId?: true
  }

  export type EventMinAggregateInputType = {
    id?: true
    title?: true
    description?: true
    startTime?: true
    endTime?: true
    location?: true
    city?: true
    state?: true
    zipCode?: true
    latitude?: true
    longitude?: true
    category?: true
    organizerId?: true
    venueId?: true
    status?: true
    created_at?: true
    updated_at?: true
  }

  export type EventMaxAggregateInputType = {
    id?: true
    title?: true
    description?: true
    startTime?: true
    endTime?: true
    location?: true
    city?: true
    state?: true
    zipCode?: true
    latitude?: true
    longitude?: true
    category?: true
    organizerId?: true
    venueId?: true
    status?: true
    created_at?: true
    updated_at?: true
  }

  export type EventCountAggregateInputType = {
    id?: true
    title?: true
    description?: true
    startTime?: true
    endTime?: true
    location?: true
    city?: true
    state?: true
    zipCode?: true
    latitude?: true
    longitude?: true
    category?: true
    organizerId?: true
    venueId?: true
    status?: true
    created_at?: true
    updated_at?: true
    _all?: true
  }

  export type EventAggregateArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Filter which Event to aggregate.
     */
    where?: EventWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Events to fetch.
     */
    orderBy?: EventOrderByWithRelationInput | EventOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the start position
     */
    cursor?: EventWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Events from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Events.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Count returned Events
    **/
    _count?: true | EventCountAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to average
    **/
    _avg?: EventAvgAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to sum
    **/
    _sum?: EventSumAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the minimum value
    **/
    _min?: EventMinAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the maximum value
    **/
    _max?: EventMaxAggregateInputType
  }

  export type GetEventAggregateType<T extends EventAggregateArgs> = {
        [P in keyof T & keyof AggregateEvent]: P extends '_count' | 'count'
      ? T[P] extends true
        ? number
        : GetScalarType<T[P], AggregateEvent[P]>
      : GetScalarType<T[P], AggregateEvent[P]>
  }




  export type EventGroupByArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    where?: EventWhereInput
    orderBy?: EventOrderByWithAggregationInput | EventOrderByWithAggregationInput[]
    by: EventScalarFieldEnum[] | EventScalarFieldEnum
    having?: EventScalarWhereWithAggregatesInput
    take?: number
    skip?: number
    _count?: EventCountAggregateInputType | true
    _avg?: EventAvgAggregateInputType
    _sum?: EventSumAggregateInputType
    _min?: EventMinAggregateInputType
    _max?: EventMaxAggregateInputType
  }

  export type EventGroupByOutputType = {
    id: number
    title: string
    description: string | null
    startTime: Date
    endTime: Date | null
    location: string | null
    city: string | null
    state: string | null
    zipCode: string | null
    latitude: number | null
    longitude: number | null
    category: string | null
    organizerId: number | null
    venueId: number | null
    status: string | null
    created_at: Date | null
    updated_at: Date | null
    _count: EventCountAggregateOutputType | null
    _avg: EventAvgAggregateOutputType | null
    _sum: EventSumAggregateOutputType | null
    _min: EventMinAggregateOutputType | null
    _max: EventMaxAggregateOutputType | null
  }

  type GetEventGroupByPayload<T extends EventGroupByArgs> = Prisma.PrismaPromise<
    Array<
      PickEnumerable<EventGroupByOutputType, T['by']> &
        {
          [P in ((keyof T) & (keyof EventGroupByOutputType))]: P extends '_count'
            ? T[P] extends boolean
              ? number
              : GetScalarType<T[P], EventGroupByOutputType[P]>
            : GetScalarType<T[P], EventGroupByOutputType[P]>
        }
      >
    >


  export type EventSelect<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetSelect<{
    id?: boolean
    title?: boolean
    description?: boolean
    startTime?: boolean
    endTime?: boolean
    location?: boolean
    city?: boolean
    state?: boolean
    zipCode?: boolean
    latitude?: boolean
    longitude?: boolean
    category?: boolean
    organizerId?: boolean
    venueId?: boolean
    status?: boolean
    created_at?: boolean
    updated_at?: boolean
    organizer?: boolean | Event$organizerArgs<ExtArgs>
    venue?: boolean | Event$venueArgs<ExtArgs>
    funalytics?: boolean | Event$funalyticsArgs<ExtArgs>
    _count?: boolean | EventCountOutputTypeDefaultArgs<ExtArgs>
  }, ExtArgs["result"]["event"]>

  export type EventSelectCreateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetSelect<{
    id?: boolean
    title?: boolean
    description?: boolean
    startTime?: boolean
    endTime?: boolean
    location?: boolean
    city?: boolean
    state?: boolean
    zipCode?: boolean
    latitude?: boolean
    longitude?: boolean
    category?: boolean
    organizerId?: boolean
    venueId?: boolean
    status?: boolean
    created_at?: boolean
    updated_at?: boolean
    organizer?: boolean | Event$organizerArgs<ExtArgs>
    venue?: boolean | Event$venueArgs<ExtArgs>
  }, ExtArgs["result"]["event"]>

  export type EventSelectUpdateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetSelect<{
    id?: boolean
    title?: boolean
    description?: boolean
    startTime?: boolean
    endTime?: boolean
    location?: boolean
    city?: boolean
    state?: boolean
    zipCode?: boolean
    latitude?: boolean
    longitude?: boolean
    category?: boolean
    organizerId?: boolean
    venueId?: boolean
    status?: boolean
    created_at?: boolean
    updated_at?: boolean
    organizer?: boolean | Event$organizerArgs<ExtArgs>
    venue?: boolean | Event$venueArgs<ExtArgs>
  }, ExtArgs["result"]["event"]>

  export type EventSelectScalar = {
    id?: boolean
    title?: boolean
    description?: boolean
    startTime?: boolean
    endTime?: boolean
    location?: boolean
    city?: boolean
    state?: boolean
    zipCode?: boolean
    latitude?: boolean
    longitude?: boolean
    category?: boolean
    organizerId?: boolean
    venueId?: boolean
    status?: boolean
    created_at?: boolean
    updated_at?: boolean
  }

  export type EventOmit<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetOmit<"id" | "title" | "description" | "startTime" | "endTime" | "location" | "city" | "state" | "zipCode" | "latitude" | "longitude" | "category" | "organizerId" | "venueId" | "status" | "created_at" | "updated_at", ExtArgs["result"]["event"]>
  export type EventInclude<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    organizer?: boolean | Event$organizerArgs<ExtArgs>
    venue?: boolean | Event$venueArgs<ExtArgs>
    funalytics?: boolean | Event$funalyticsArgs<ExtArgs>
    _count?: boolean | EventCountOutputTypeDefaultArgs<ExtArgs>
  }
  export type EventIncludeCreateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    organizer?: boolean | Event$organizerArgs<ExtArgs>
    venue?: boolean | Event$venueArgs<ExtArgs>
  }
  export type EventIncludeUpdateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    organizer?: boolean | Event$organizerArgs<ExtArgs>
    venue?: boolean | Event$venueArgs<ExtArgs>
  }

  export type $EventPayload<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    name: "Event"
    objects: {
      organizer: Prisma.$UserPayload<ExtArgs> | null
      venue: Prisma.$VenuePayload<ExtArgs> | null
      funalytics: Prisma.$FunalyticsScorePayload<ExtArgs>[]
    }
    scalars: $Extensions.GetPayloadResult<{
      id: number
      title: string
      description: string | null
      startTime: Date
      endTime: Date | null
      location: string | null
      city: string | null
      state: string | null
      zipCode: string | null
      latitude: number | null
      longitude: number | null
      category: string | null
      organizerId: number | null
      venueId: number | null
      status: string | null
      created_at: Date | null
      updated_at: Date | null
    }, ExtArgs["result"]["event"]>
    composites: {}
  }

  type EventGetPayload<S extends boolean | null | undefined | EventDefaultArgs> = $Result.GetResult<Prisma.$EventPayload, S>

  type EventCountArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> =
    Omit<EventFindManyArgs, 'select' | 'include' | 'distinct' | 'omit'> & {
      select?: EventCountAggregateInputType | true
    }

  export interface EventDelegate<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs, GlobalOmitOptions = {}> {
    [K: symbol]: { types: Prisma.TypeMap<ExtArgs>['model']['Event'], meta: { name: 'Event' } }
    /**
     * Find zero or one Event that matches the filter.
     * @param {EventFindUniqueArgs} args - Arguments to find a Event
     * @example
     * // Get one Event
     * const event = await prisma.event.findUnique({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findUnique<T extends EventFindUniqueArgs>(args: SelectSubset<T, EventFindUniqueArgs<ExtArgs>>): Prisma__EventClient<$Result.GetResult<Prisma.$EventPayload<ExtArgs>, T, "findUnique", GlobalOmitOptions> | null, null, ExtArgs, GlobalOmitOptions>

    /**
     * Find one Event that matches the filter or throw an error with `error.code='P2025'`
     * if no matches were found.
     * @param {EventFindUniqueOrThrowArgs} args - Arguments to find a Event
     * @example
     * // Get one Event
     * const event = await prisma.event.findUniqueOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findUniqueOrThrow<T extends EventFindUniqueOrThrowArgs>(args: SelectSubset<T, EventFindUniqueOrThrowArgs<ExtArgs>>): Prisma__EventClient<$Result.GetResult<Prisma.$EventPayload<ExtArgs>, T, "findUniqueOrThrow", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Find the first Event that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {EventFindFirstArgs} args - Arguments to find a Event
     * @example
     * // Get one Event
     * const event = await prisma.event.findFirst({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findFirst<T extends EventFindFirstArgs>(args?: SelectSubset<T, EventFindFirstArgs<ExtArgs>>): Prisma__EventClient<$Result.GetResult<Prisma.$EventPayload<ExtArgs>, T, "findFirst", GlobalOmitOptions> | null, null, ExtArgs, GlobalOmitOptions>

    /**
     * Find the first Event that matches the filter or
     * throw `PrismaKnownClientError` with `P2025` code if no matches were found.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {EventFindFirstOrThrowArgs} args - Arguments to find a Event
     * @example
     * // Get one Event
     * const event = await prisma.event.findFirstOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findFirstOrThrow<T extends EventFindFirstOrThrowArgs>(args?: SelectSubset<T, EventFindFirstOrThrowArgs<ExtArgs>>): Prisma__EventClient<$Result.GetResult<Prisma.$EventPayload<ExtArgs>, T, "findFirstOrThrow", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Find zero or more Events that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {EventFindManyArgs} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all Events
     * const events = await prisma.event.findMany()
     * 
     * // Get first 10 Events
     * const events = await prisma.event.findMany({ take: 10 })
     * 
     * // Only select the `id`
     * const eventWithIdOnly = await prisma.event.findMany({ select: { id: true } })
     * 
     */
    findMany<T extends EventFindManyArgs>(args?: SelectSubset<T, EventFindManyArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$EventPayload<ExtArgs>, T, "findMany", GlobalOmitOptions>>

    /**
     * Create a Event.
     * @param {EventCreateArgs} args - Arguments to create a Event.
     * @example
     * // Create one Event
     * const Event = await prisma.event.create({
     *   data: {
     *     // ... data to create a Event
     *   }
     * })
     * 
     */
    create<T extends EventCreateArgs>(args: SelectSubset<T, EventCreateArgs<ExtArgs>>): Prisma__EventClient<$Result.GetResult<Prisma.$EventPayload<ExtArgs>, T, "create", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Create many Events.
     * @param {EventCreateManyArgs} args - Arguments to create many Events.
     * @example
     * // Create many Events
     * const event = await prisma.event.createMany({
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     *     
     */
    createMany<T extends EventCreateManyArgs>(args?: SelectSubset<T, EventCreateManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>

    /**
     * Create many Events and returns the data saved in the database.
     * @param {EventCreateManyAndReturnArgs} args - Arguments to create many Events.
     * @example
     * // Create many Events
     * const event = await prisma.event.createManyAndReturn({
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * 
     * // Create many Events and only return the `id`
     * const eventWithIdOnly = await prisma.event.createManyAndReturn({
     *   select: { id: true },
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * 
     */
    createManyAndReturn<T extends EventCreateManyAndReturnArgs>(args?: SelectSubset<T, EventCreateManyAndReturnArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$EventPayload<ExtArgs>, T, "createManyAndReturn", GlobalOmitOptions>>

    /**
     * Delete a Event.
     * @param {EventDeleteArgs} args - Arguments to delete one Event.
     * @example
     * // Delete one Event
     * const Event = await prisma.event.delete({
     *   where: {
     *     // ... filter to delete one Event
     *   }
     * })
     * 
     */
    delete<T extends EventDeleteArgs>(args: SelectSubset<T, EventDeleteArgs<ExtArgs>>): Prisma__EventClient<$Result.GetResult<Prisma.$EventPayload<ExtArgs>, T, "delete", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Update one Event.
     * @param {EventUpdateArgs} args - Arguments to update one Event.
     * @example
     * // Update one Event
     * const event = await prisma.event.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    update<T extends EventUpdateArgs>(args: SelectSubset<T, EventUpdateArgs<ExtArgs>>): Prisma__EventClient<$Result.GetResult<Prisma.$EventPayload<ExtArgs>, T, "update", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Delete zero or more Events.
     * @param {EventDeleteManyArgs} args - Arguments to filter Events to delete.
     * @example
     * // Delete a few Events
     * const { count } = await prisma.event.deleteMany({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     * 
     */
    deleteMany<T extends EventDeleteManyArgs>(args?: SelectSubset<T, EventDeleteManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>

    /**
     * Update zero or more Events.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {EventUpdateManyArgs} args - Arguments to update one or more rows.
     * @example
     * // Update many Events
     * const event = await prisma.event.updateMany({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    updateMany<T extends EventUpdateManyArgs>(args: SelectSubset<T, EventUpdateManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>

    /**
     * Update zero or more Events and returns the data updated in the database.
     * @param {EventUpdateManyAndReturnArgs} args - Arguments to update many Events.
     * @example
     * // Update many Events
     * const event = await prisma.event.updateManyAndReturn({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * 
     * // Update zero or more Events and only return the `id`
     * const eventWithIdOnly = await prisma.event.updateManyAndReturn({
     *   select: { id: true },
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * 
     */
    updateManyAndReturn<T extends EventUpdateManyAndReturnArgs>(args: SelectSubset<T, EventUpdateManyAndReturnArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$EventPayload<ExtArgs>, T, "updateManyAndReturn", GlobalOmitOptions>>

    /**
     * Create or update one Event.
     * @param {EventUpsertArgs} args - Arguments to update or create a Event.
     * @example
     * // Update or create a Event
     * const event = await prisma.event.upsert({
     *   create: {
     *     // ... data to create a Event
     *   },
     *   update: {
     *     // ... in case it already exists, update
     *   },
     *   where: {
     *     // ... the filter for the Event we want to update
     *   }
     * })
     */
    upsert<T extends EventUpsertArgs>(args: SelectSubset<T, EventUpsertArgs<ExtArgs>>): Prisma__EventClient<$Result.GetResult<Prisma.$EventPayload<ExtArgs>, T, "upsert", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>


    /**
     * Count the number of Events.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {EventCountArgs} args - Arguments to filter Events to count.
     * @example
     * // Count the number of Events
     * const count = await prisma.event.count({
     *   where: {
     *     // ... the filter for the Events we want to count
     *   }
     * })
    **/
    count<T extends EventCountArgs>(
      args?: Subset<T, EventCountArgs>,
    ): Prisma.PrismaPromise<
      T extends $Utils.Record<'select', any>
        ? T['select'] extends true
          ? number
          : GetScalarType<T['select'], EventCountAggregateOutputType>
        : number
    >

    /**
     * Allows you to perform aggregations operations on a Event.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {EventAggregateArgs} args - Select which aggregations you would like to apply and on what fields.
     * @example
     * // Ordered by age ascending
     * // Where email contains prisma.io
     * // Limited to the 10 users
     * const aggregations = await prisma.user.aggregate({
     *   _avg: {
     *     age: true,
     *   },
     *   where: {
     *     email: {
     *       contains: "prisma.io",
     *     },
     *   },
     *   orderBy: {
     *     age: "asc",
     *   },
     *   take: 10,
     * })
    **/
    aggregate<T extends EventAggregateArgs>(args: Subset<T, EventAggregateArgs>): Prisma.PrismaPromise<GetEventAggregateType<T>>

    /**
     * Group by Event.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {EventGroupByArgs} args - Group by arguments.
     * @example
     * // Group by city, order by createdAt, get count
     * const result = await prisma.user.groupBy({
     *   by: ['city', 'createdAt'],
     *   orderBy: {
     *     createdAt: true
     *   },
     *   _count: {
     *     _all: true
     *   },
     * })
     * 
    **/
    groupBy<
      T extends EventGroupByArgs,
      HasSelectOrTake extends Or<
        Extends<'skip', Keys<T>>,
        Extends<'take', Keys<T>>
      >,
      OrderByArg extends True extends HasSelectOrTake
        ? { orderBy: EventGroupByArgs['orderBy'] }
        : { orderBy?: EventGroupByArgs['orderBy'] },
      OrderFields extends ExcludeUnderscoreKeys<Keys<MaybeTupleToUnion<T['orderBy']>>>,
      ByFields extends MaybeTupleToUnion<T['by']>,
      ByValid extends Has<ByFields, OrderFields>,
      HavingFields extends GetHavingFields<T['having']>,
      HavingValid extends Has<ByFields, HavingFields>,
      ByEmpty extends T['by'] extends never[] ? True : False,
      InputErrors extends ByEmpty extends True
      ? `Error: "by" must not be empty.`
      : HavingValid extends False
      ? {
          [P in HavingFields]: P extends ByFields
            ? never
            : P extends string
            ? `Error: Field "${P}" used in "having" needs to be provided in "by".`
            : [
                Error,
                'Field ',
                P,
                ` in "having" needs to be provided in "by"`,
              ]
        }[HavingFields]
      : 'take' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "take", you also need to provide "orderBy"'
      : 'skip' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "skip", you also need to provide "orderBy"'
      : ByValid extends True
      ? {}
      : {
          [P in OrderFields]: P extends ByFields
            ? never
            : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
        }[OrderFields]
    >(args: SubsetIntersection<T, EventGroupByArgs, OrderByArg> & InputErrors): {} extends InputErrors ? GetEventGroupByPayload<T> : Prisma.PrismaPromise<InputErrors>
  /**
   * Fields of the Event model
   */
  readonly fields: EventFieldRefs;
  }

  /**
   * The delegate class that acts as a "Promise-like" for Event.
   * Why is this prefixed with `Prisma__`?
   * Because we want to prevent naming conflicts as mentioned in
   * https://github.com/prisma/prisma-client-js/issues/707
   */
  export interface Prisma__EventClient<T, Null = never, ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs, GlobalOmitOptions = {}> extends Prisma.PrismaPromise<T> {
    readonly [Symbol.toStringTag]: "PrismaPromise"
    organizer<T extends Event$organizerArgs<ExtArgs> = {}>(args?: Subset<T, Event$organizerArgs<ExtArgs>>): Prisma__UserClient<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "findUniqueOrThrow", GlobalOmitOptions> | null, null, ExtArgs, GlobalOmitOptions>
    venue<T extends Event$venueArgs<ExtArgs> = {}>(args?: Subset<T, Event$venueArgs<ExtArgs>>): Prisma__VenueClient<$Result.GetResult<Prisma.$VenuePayload<ExtArgs>, T, "findUniqueOrThrow", GlobalOmitOptions> | null, null, ExtArgs, GlobalOmitOptions>
    funalytics<T extends Event$funalyticsArgs<ExtArgs> = {}>(args?: Subset<T, Event$funalyticsArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$FunalyticsScorePayload<ExtArgs>, T, "findMany", GlobalOmitOptions> | Null>
    /**
     * Attaches callbacks for the resolution and/or rejection of the Promise.
     * @param onfulfilled The callback to execute when the Promise is resolved.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of which ever callback is executed.
     */
    then<TResult1 = T, TResult2 = never>(onfulfilled?: ((value: T) => TResult1 | PromiseLike<TResult1>) | undefined | null, onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | undefined | null): $Utils.JsPromise<TResult1 | TResult2>
    /**
     * Attaches a callback for only the rejection of the Promise.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of the callback.
     */
    catch<TResult = never>(onrejected?: ((reason: any) => TResult | PromiseLike<TResult>) | undefined | null): $Utils.JsPromise<T | TResult>
    /**
     * Attaches a callback that is invoked when the Promise is settled (fulfilled or rejected). The
     * resolved value cannot be modified from the callback.
     * @param onfinally The callback to execute when the Promise is settled (fulfilled or rejected).
     * @returns A Promise for the completion of the callback.
     */
    finally(onfinally?: (() => void) | undefined | null): $Utils.JsPromise<T>
  }




  /**
   * Fields of the Event model
   */
  interface EventFieldRefs {
    readonly id: FieldRef<"Event", 'Int'>
    readonly title: FieldRef<"Event", 'String'>
    readonly description: FieldRef<"Event", 'String'>
    readonly startTime: FieldRef<"Event", 'DateTime'>
    readonly endTime: FieldRef<"Event", 'DateTime'>
    readonly location: FieldRef<"Event", 'String'>
    readonly city: FieldRef<"Event", 'String'>
    readonly state: FieldRef<"Event", 'String'>
    readonly zipCode: FieldRef<"Event", 'String'>
    readonly latitude: FieldRef<"Event", 'Float'>
    readonly longitude: FieldRef<"Event", 'Float'>
    readonly category: FieldRef<"Event", 'String'>
    readonly organizerId: FieldRef<"Event", 'Int'>
    readonly venueId: FieldRef<"Event", 'Int'>
    readonly status: FieldRef<"Event", 'String'>
    readonly created_at: FieldRef<"Event", 'DateTime'>
    readonly updated_at: FieldRef<"Event", 'DateTime'>
  }
    

  // Custom InputTypes
  /**
   * Event findUnique
   */
  export type EventFindUniqueArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Event
     */
    select?: EventSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Event
     */
    omit?: EventOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: EventInclude<ExtArgs> | null
    /**
     * Filter, which Event to fetch.
     */
    where: EventWhereUniqueInput
  }

  /**
   * Event findUniqueOrThrow
   */
  export type EventFindUniqueOrThrowArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Event
     */
    select?: EventSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Event
     */
    omit?: EventOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: EventInclude<ExtArgs> | null
    /**
     * Filter, which Event to fetch.
     */
    where: EventWhereUniqueInput
  }

  /**
   * Event findFirst
   */
  export type EventFindFirstArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Event
     */
    select?: EventSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Event
     */
    omit?: EventOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: EventInclude<ExtArgs> | null
    /**
     * Filter, which Event to fetch.
     */
    where?: EventWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Events to fetch.
     */
    orderBy?: EventOrderByWithRelationInput | EventOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for Events.
     */
    cursor?: EventWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Events from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Events.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of Events.
     */
    distinct?: EventScalarFieldEnum | EventScalarFieldEnum[]
  }

  /**
   * Event findFirstOrThrow
   */
  export type EventFindFirstOrThrowArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Event
     */
    select?: EventSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Event
     */
    omit?: EventOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: EventInclude<ExtArgs> | null
    /**
     * Filter, which Event to fetch.
     */
    where?: EventWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Events to fetch.
     */
    orderBy?: EventOrderByWithRelationInput | EventOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for Events.
     */
    cursor?: EventWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Events from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Events.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of Events.
     */
    distinct?: EventScalarFieldEnum | EventScalarFieldEnum[]
  }

  /**
   * Event findMany
   */
  export type EventFindManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Event
     */
    select?: EventSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Event
     */
    omit?: EventOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: EventInclude<ExtArgs> | null
    /**
     * Filter, which Events to fetch.
     */
    where?: EventWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Events to fetch.
     */
    orderBy?: EventOrderByWithRelationInput | EventOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for listing Events.
     */
    cursor?: EventWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Events from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Events.
     */
    skip?: number
    distinct?: EventScalarFieldEnum | EventScalarFieldEnum[]
  }

  /**
   * Event create
   */
  export type EventCreateArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Event
     */
    select?: EventSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Event
     */
    omit?: EventOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: EventInclude<ExtArgs> | null
    /**
     * The data needed to create a Event.
     */
    data: XOR<EventCreateInput, EventUncheckedCreateInput>
  }

  /**
   * Event createMany
   */
  export type EventCreateManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * The data used to create many Events.
     */
    data: EventCreateManyInput | EventCreateManyInput[]
    skipDuplicates?: boolean
  }

  /**
   * Event createManyAndReturn
   */
  export type EventCreateManyAndReturnArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Event
     */
    select?: EventSelectCreateManyAndReturn<ExtArgs> | null
    /**
     * Omit specific fields from the Event
     */
    omit?: EventOmit<ExtArgs> | null
    /**
     * The data used to create many Events.
     */
    data: EventCreateManyInput | EventCreateManyInput[]
    skipDuplicates?: boolean
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: EventIncludeCreateManyAndReturn<ExtArgs> | null
  }

  /**
   * Event update
   */
  export type EventUpdateArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Event
     */
    select?: EventSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Event
     */
    omit?: EventOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: EventInclude<ExtArgs> | null
    /**
     * The data needed to update a Event.
     */
    data: XOR<EventUpdateInput, EventUncheckedUpdateInput>
    /**
     * Choose, which Event to update.
     */
    where: EventWhereUniqueInput
  }

  /**
   * Event updateMany
   */
  export type EventUpdateManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * The data used to update Events.
     */
    data: XOR<EventUpdateManyMutationInput, EventUncheckedUpdateManyInput>
    /**
     * Filter which Events to update
     */
    where?: EventWhereInput
    /**
     * Limit how many Events to update.
     */
    limit?: number
  }

  /**
   * Event updateManyAndReturn
   */
  export type EventUpdateManyAndReturnArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Event
     */
    select?: EventSelectUpdateManyAndReturn<ExtArgs> | null
    /**
     * Omit specific fields from the Event
     */
    omit?: EventOmit<ExtArgs> | null
    /**
     * The data used to update Events.
     */
    data: XOR<EventUpdateManyMutationInput, EventUncheckedUpdateManyInput>
    /**
     * Filter which Events to update
     */
    where?: EventWhereInput
    /**
     * Limit how many Events to update.
     */
    limit?: number
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: EventIncludeUpdateManyAndReturn<ExtArgs> | null
  }

  /**
   * Event upsert
   */
  export type EventUpsertArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Event
     */
    select?: EventSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Event
     */
    omit?: EventOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: EventInclude<ExtArgs> | null
    /**
     * The filter to search for the Event to update in case it exists.
     */
    where: EventWhereUniqueInput
    /**
     * In case the Event found by the `where` argument doesn't exist, create a new Event with this data.
     */
    create: XOR<EventCreateInput, EventUncheckedCreateInput>
    /**
     * In case the Event was found with the provided `where` argument, update it with this data.
     */
    update: XOR<EventUpdateInput, EventUncheckedUpdateInput>
  }

  /**
   * Event delete
   */
  export type EventDeleteArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Event
     */
    select?: EventSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Event
     */
    omit?: EventOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: EventInclude<ExtArgs> | null
    /**
     * Filter which Event to delete.
     */
    where: EventWhereUniqueInput
  }

  /**
   * Event deleteMany
   */
  export type EventDeleteManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Filter which Events to delete
     */
    where?: EventWhereInput
    /**
     * Limit how many Events to delete.
     */
    limit?: number
  }

  /**
   * Event.organizer
   */
  export type Event$organizerArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the User
     */
    select?: UserSelect<ExtArgs> | null
    /**
     * Omit specific fields from the User
     */
    omit?: UserOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: UserInclude<ExtArgs> | null
    where?: UserWhereInput
  }

  /**
   * Event.venue
   */
  export type Event$venueArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Venue
     */
    select?: VenueSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Venue
     */
    omit?: VenueOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: VenueInclude<ExtArgs> | null
    where?: VenueWhereInput
  }

  /**
   * Event.funalytics
   */
  export type Event$funalyticsArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the FunalyticsScore
     */
    select?: FunalyticsScoreSelect<ExtArgs> | null
    /**
     * Omit specific fields from the FunalyticsScore
     */
    omit?: FunalyticsScoreOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: FunalyticsScoreInclude<ExtArgs> | null
    where?: FunalyticsScoreWhereInput
    orderBy?: FunalyticsScoreOrderByWithRelationInput | FunalyticsScoreOrderByWithRelationInput[]
    cursor?: FunalyticsScoreWhereUniqueInput
    take?: number
    skip?: number
    distinct?: FunalyticsScoreScalarFieldEnum | FunalyticsScoreScalarFieldEnum[]
  }

  /**
   * Event without action
   */
  export type EventDefaultArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Event
     */
    select?: EventSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Event
     */
    omit?: EventOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: EventInclude<ExtArgs> | null
  }


  /**
   * Model User
   */

  export type AggregateUser = {
    _count: UserCountAggregateOutputType | null
    _avg: UserAvgAggregateOutputType | null
    _sum: UserSumAggregateOutputType | null
    _min: UserMinAggregateOutputType | null
    _max: UserMaxAggregateOutputType | null
  }

  export type UserAvgAggregateOutputType = {
    id: number | null
  }

  export type UserSumAggregateOutputType = {
    id: number | null
  }

  export type UserMinAggregateOutputType = {
    id: number | null
    first_name: string | null
    last_name: string | null
    company_name: string | null
    email: string | null
    password_hash: string | null
    phone: string | null
    is_organizer: boolean | null
    is_sponsor: boolean | null
    is_vendor: boolean | null
    is_admin: boolean | null
    is_active: boolean | null
    created_at: Date | null
    updated_at: Date | null
  }

  export type UserMaxAggregateOutputType = {
    id: number | null
    first_name: string | null
    last_name: string | null
    company_name: string | null
    email: string | null
    password_hash: string | null
    phone: string | null
    is_organizer: boolean | null
    is_sponsor: boolean | null
    is_vendor: boolean | null
    is_admin: boolean | null
    is_active: boolean | null
    created_at: Date | null
    updated_at: Date | null
  }

  export type UserCountAggregateOutputType = {
    id: number
    first_name: number
    last_name: number
    company_name: number
    email: number
    password_hash: number
    phone: number
    is_organizer: number
    is_sponsor: number
    is_vendor: number
    is_admin: number
    is_active: number
    created_at: number
    updated_at: number
    _all: number
  }


  export type UserAvgAggregateInputType = {
    id?: true
  }

  export type UserSumAggregateInputType = {
    id?: true
  }

  export type UserMinAggregateInputType = {
    id?: true
    first_name?: true
    last_name?: true
    company_name?: true
    email?: true
    password_hash?: true
    phone?: true
    is_organizer?: true
    is_sponsor?: true
    is_vendor?: true
    is_admin?: true
    is_active?: true
    created_at?: true
    updated_at?: true
  }

  export type UserMaxAggregateInputType = {
    id?: true
    first_name?: true
    last_name?: true
    company_name?: true
    email?: true
    password_hash?: true
    phone?: true
    is_organizer?: true
    is_sponsor?: true
    is_vendor?: true
    is_admin?: true
    is_active?: true
    created_at?: true
    updated_at?: true
  }

  export type UserCountAggregateInputType = {
    id?: true
    first_name?: true
    last_name?: true
    company_name?: true
    email?: true
    password_hash?: true
    phone?: true
    is_organizer?: true
    is_sponsor?: true
    is_vendor?: true
    is_admin?: true
    is_active?: true
    created_at?: true
    updated_at?: true
    _all?: true
  }

  export type UserAggregateArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Filter which User to aggregate.
     */
    where?: UserWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Users to fetch.
     */
    orderBy?: UserOrderByWithRelationInput | UserOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the start position
     */
    cursor?: UserWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Users from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Users.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Count returned Users
    **/
    _count?: true | UserCountAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to average
    **/
    _avg?: UserAvgAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to sum
    **/
    _sum?: UserSumAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the minimum value
    **/
    _min?: UserMinAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the maximum value
    **/
    _max?: UserMaxAggregateInputType
  }

  export type GetUserAggregateType<T extends UserAggregateArgs> = {
        [P in keyof T & keyof AggregateUser]: P extends '_count' | 'count'
      ? T[P] extends true
        ? number
        : GetScalarType<T[P], AggregateUser[P]>
      : GetScalarType<T[P], AggregateUser[P]>
  }




  export type UserGroupByArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    where?: UserWhereInput
    orderBy?: UserOrderByWithAggregationInput | UserOrderByWithAggregationInput[]
    by: UserScalarFieldEnum[] | UserScalarFieldEnum
    having?: UserScalarWhereWithAggregatesInput
    take?: number
    skip?: number
    _count?: UserCountAggregateInputType | true
    _avg?: UserAvgAggregateInputType
    _sum?: UserSumAggregateInputType
    _min?: UserMinAggregateInputType
    _max?: UserMaxAggregateInputType
  }

  export type UserGroupByOutputType = {
    id: number
    first_name: string | null
    last_name: string | null
    company_name: string | null
    email: string
    password_hash: string | null
    phone: string | null
    is_organizer: boolean | null
    is_sponsor: boolean | null
    is_vendor: boolean | null
    is_admin: boolean | null
    is_active: boolean | null
    created_at: Date | null
    updated_at: Date | null
    _count: UserCountAggregateOutputType | null
    _avg: UserAvgAggregateOutputType | null
    _sum: UserSumAggregateOutputType | null
    _min: UserMinAggregateOutputType | null
    _max: UserMaxAggregateOutputType | null
  }

  type GetUserGroupByPayload<T extends UserGroupByArgs> = Prisma.PrismaPromise<
    Array<
      PickEnumerable<UserGroupByOutputType, T['by']> &
        {
          [P in ((keyof T) & (keyof UserGroupByOutputType))]: P extends '_count'
            ? T[P] extends boolean
              ? number
              : GetScalarType<T[P], UserGroupByOutputType[P]>
            : GetScalarType<T[P], UserGroupByOutputType[P]>
        }
      >
    >


  export type UserSelect<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetSelect<{
    id?: boolean
    first_name?: boolean
    last_name?: boolean
    company_name?: boolean
    email?: boolean
    password_hash?: boolean
    phone?: boolean
    is_organizer?: boolean
    is_sponsor?: boolean
    is_vendor?: boolean
    is_admin?: boolean
    is_active?: boolean
    created_at?: boolean
    updated_at?: boolean
    events?: boolean | User$eventsArgs<ExtArgs>
    _count?: boolean | UserCountOutputTypeDefaultArgs<ExtArgs>
  }, ExtArgs["result"]["user"]>

  export type UserSelectCreateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetSelect<{
    id?: boolean
    first_name?: boolean
    last_name?: boolean
    company_name?: boolean
    email?: boolean
    password_hash?: boolean
    phone?: boolean
    is_organizer?: boolean
    is_sponsor?: boolean
    is_vendor?: boolean
    is_admin?: boolean
    is_active?: boolean
    created_at?: boolean
    updated_at?: boolean
  }, ExtArgs["result"]["user"]>

  export type UserSelectUpdateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetSelect<{
    id?: boolean
    first_name?: boolean
    last_name?: boolean
    company_name?: boolean
    email?: boolean
    password_hash?: boolean
    phone?: boolean
    is_organizer?: boolean
    is_sponsor?: boolean
    is_vendor?: boolean
    is_admin?: boolean
    is_active?: boolean
    created_at?: boolean
    updated_at?: boolean
  }, ExtArgs["result"]["user"]>

  export type UserSelectScalar = {
    id?: boolean
    first_name?: boolean
    last_name?: boolean
    company_name?: boolean
    email?: boolean
    password_hash?: boolean
    phone?: boolean
    is_organizer?: boolean
    is_sponsor?: boolean
    is_vendor?: boolean
    is_admin?: boolean
    is_active?: boolean
    created_at?: boolean
    updated_at?: boolean
  }

  export type UserOmit<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetOmit<"id" | "first_name" | "last_name" | "company_name" | "email" | "password_hash" | "phone" | "is_organizer" | "is_sponsor" | "is_vendor" | "is_admin" | "is_active" | "created_at" | "updated_at", ExtArgs["result"]["user"]>
  export type UserInclude<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    events?: boolean | User$eventsArgs<ExtArgs>
    _count?: boolean | UserCountOutputTypeDefaultArgs<ExtArgs>
  }
  export type UserIncludeCreateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {}
  export type UserIncludeUpdateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {}

  export type $UserPayload<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    name: "User"
    objects: {
      events: Prisma.$EventPayload<ExtArgs>[]
    }
    scalars: $Extensions.GetPayloadResult<{
      id: number
      first_name: string | null
      last_name: string | null
      company_name: string | null
      email: string
      password_hash: string | null
      phone: string | null
      is_organizer: boolean | null
      is_sponsor: boolean | null
      is_vendor: boolean | null
      is_admin: boolean | null
      is_active: boolean | null
      created_at: Date | null
      updated_at: Date | null
    }, ExtArgs["result"]["user"]>
    composites: {}
  }

  type UserGetPayload<S extends boolean | null | undefined | UserDefaultArgs> = $Result.GetResult<Prisma.$UserPayload, S>

  type UserCountArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> =
    Omit<UserFindManyArgs, 'select' | 'include' | 'distinct' | 'omit'> & {
      select?: UserCountAggregateInputType | true
    }

  export interface UserDelegate<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs, GlobalOmitOptions = {}> {
    [K: symbol]: { types: Prisma.TypeMap<ExtArgs>['model']['User'], meta: { name: 'User' } }
    /**
     * Find zero or one User that matches the filter.
     * @param {UserFindUniqueArgs} args - Arguments to find a User
     * @example
     * // Get one User
     * const user = await prisma.user.findUnique({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findUnique<T extends UserFindUniqueArgs>(args: SelectSubset<T, UserFindUniqueArgs<ExtArgs>>): Prisma__UserClient<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "findUnique", GlobalOmitOptions> | null, null, ExtArgs, GlobalOmitOptions>

    /**
     * Find one User that matches the filter or throw an error with `error.code='P2025'`
     * if no matches were found.
     * @param {UserFindUniqueOrThrowArgs} args - Arguments to find a User
     * @example
     * // Get one User
     * const user = await prisma.user.findUniqueOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findUniqueOrThrow<T extends UserFindUniqueOrThrowArgs>(args: SelectSubset<T, UserFindUniqueOrThrowArgs<ExtArgs>>): Prisma__UserClient<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "findUniqueOrThrow", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Find the first User that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {UserFindFirstArgs} args - Arguments to find a User
     * @example
     * // Get one User
     * const user = await prisma.user.findFirst({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findFirst<T extends UserFindFirstArgs>(args?: SelectSubset<T, UserFindFirstArgs<ExtArgs>>): Prisma__UserClient<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "findFirst", GlobalOmitOptions> | null, null, ExtArgs, GlobalOmitOptions>

    /**
     * Find the first User that matches the filter or
     * throw `PrismaKnownClientError` with `P2025` code if no matches were found.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {UserFindFirstOrThrowArgs} args - Arguments to find a User
     * @example
     * // Get one User
     * const user = await prisma.user.findFirstOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findFirstOrThrow<T extends UserFindFirstOrThrowArgs>(args?: SelectSubset<T, UserFindFirstOrThrowArgs<ExtArgs>>): Prisma__UserClient<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "findFirstOrThrow", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Find zero or more Users that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {UserFindManyArgs} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all Users
     * const users = await prisma.user.findMany()
     * 
     * // Get first 10 Users
     * const users = await prisma.user.findMany({ take: 10 })
     * 
     * // Only select the `id`
     * const userWithIdOnly = await prisma.user.findMany({ select: { id: true } })
     * 
     */
    findMany<T extends UserFindManyArgs>(args?: SelectSubset<T, UserFindManyArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "findMany", GlobalOmitOptions>>

    /**
     * Create a User.
     * @param {UserCreateArgs} args - Arguments to create a User.
     * @example
     * // Create one User
     * const User = await prisma.user.create({
     *   data: {
     *     // ... data to create a User
     *   }
     * })
     * 
     */
    create<T extends UserCreateArgs>(args: SelectSubset<T, UserCreateArgs<ExtArgs>>): Prisma__UserClient<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "create", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Create many Users.
     * @param {UserCreateManyArgs} args - Arguments to create many Users.
     * @example
     * // Create many Users
     * const user = await prisma.user.createMany({
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     *     
     */
    createMany<T extends UserCreateManyArgs>(args?: SelectSubset<T, UserCreateManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>

    /**
     * Create many Users and returns the data saved in the database.
     * @param {UserCreateManyAndReturnArgs} args - Arguments to create many Users.
     * @example
     * // Create many Users
     * const user = await prisma.user.createManyAndReturn({
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * 
     * // Create many Users and only return the `id`
     * const userWithIdOnly = await prisma.user.createManyAndReturn({
     *   select: { id: true },
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * 
     */
    createManyAndReturn<T extends UserCreateManyAndReturnArgs>(args?: SelectSubset<T, UserCreateManyAndReturnArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "createManyAndReturn", GlobalOmitOptions>>

    /**
     * Delete a User.
     * @param {UserDeleteArgs} args - Arguments to delete one User.
     * @example
     * // Delete one User
     * const User = await prisma.user.delete({
     *   where: {
     *     // ... filter to delete one User
     *   }
     * })
     * 
     */
    delete<T extends UserDeleteArgs>(args: SelectSubset<T, UserDeleteArgs<ExtArgs>>): Prisma__UserClient<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "delete", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Update one User.
     * @param {UserUpdateArgs} args - Arguments to update one User.
     * @example
     * // Update one User
     * const user = await prisma.user.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    update<T extends UserUpdateArgs>(args: SelectSubset<T, UserUpdateArgs<ExtArgs>>): Prisma__UserClient<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "update", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Delete zero or more Users.
     * @param {UserDeleteManyArgs} args - Arguments to filter Users to delete.
     * @example
     * // Delete a few Users
     * const { count } = await prisma.user.deleteMany({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     * 
     */
    deleteMany<T extends UserDeleteManyArgs>(args?: SelectSubset<T, UserDeleteManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>

    /**
     * Update zero or more Users.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {UserUpdateManyArgs} args - Arguments to update one or more rows.
     * @example
     * // Update many Users
     * const user = await prisma.user.updateMany({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    updateMany<T extends UserUpdateManyArgs>(args: SelectSubset<T, UserUpdateManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>

    /**
     * Update zero or more Users and returns the data updated in the database.
     * @param {UserUpdateManyAndReturnArgs} args - Arguments to update many Users.
     * @example
     * // Update many Users
     * const user = await prisma.user.updateManyAndReturn({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * 
     * // Update zero or more Users and only return the `id`
     * const userWithIdOnly = await prisma.user.updateManyAndReturn({
     *   select: { id: true },
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * 
     */
    updateManyAndReturn<T extends UserUpdateManyAndReturnArgs>(args: SelectSubset<T, UserUpdateManyAndReturnArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "updateManyAndReturn", GlobalOmitOptions>>

    /**
     * Create or update one User.
     * @param {UserUpsertArgs} args - Arguments to update or create a User.
     * @example
     * // Update or create a User
     * const user = await prisma.user.upsert({
     *   create: {
     *     // ... data to create a User
     *   },
     *   update: {
     *     // ... in case it already exists, update
     *   },
     *   where: {
     *     // ... the filter for the User we want to update
     *   }
     * })
     */
    upsert<T extends UserUpsertArgs>(args: SelectSubset<T, UserUpsertArgs<ExtArgs>>): Prisma__UserClient<$Result.GetResult<Prisma.$UserPayload<ExtArgs>, T, "upsert", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>


    /**
     * Count the number of Users.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {UserCountArgs} args - Arguments to filter Users to count.
     * @example
     * // Count the number of Users
     * const count = await prisma.user.count({
     *   where: {
     *     // ... the filter for the Users we want to count
     *   }
     * })
    **/
    count<T extends UserCountArgs>(
      args?: Subset<T, UserCountArgs>,
    ): Prisma.PrismaPromise<
      T extends $Utils.Record<'select', any>
        ? T['select'] extends true
          ? number
          : GetScalarType<T['select'], UserCountAggregateOutputType>
        : number
    >

    /**
     * Allows you to perform aggregations operations on a User.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {UserAggregateArgs} args - Select which aggregations you would like to apply and on what fields.
     * @example
     * // Ordered by age ascending
     * // Where email contains prisma.io
     * // Limited to the 10 users
     * const aggregations = await prisma.user.aggregate({
     *   _avg: {
     *     age: true,
     *   },
     *   where: {
     *     email: {
     *       contains: "prisma.io",
     *     },
     *   },
     *   orderBy: {
     *     age: "asc",
     *   },
     *   take: 10,
     * })
    **/
    aggregate<T extends UserAggregateArgs>(args: Subset<T, UserAggregateArgs>): Prisma.PrismaPromise<GetUserAggregateType<T>>

    /**
     * Group by User.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {UserGroupByArgs} args - Group by arguments.
     * @example
     * // Group by city, order by createdAt, get count
     * const result = await prisma.user.groupBy({
     *   by: ['city', 'createdAt'],
     *   orderBy: {
     *     createdAt: true
     *   },
     *   _count: {
     *     _all: true
     *   },
     * })
     * 
    **/
    groupBy<
      T extends UserGroupByArgs,
      HasSelectOrTake extends Or<
        Extends<'skip', Keys<T>>,
        Extends<'take', Keys<T>>
      >,
      OrderByArg extends True extends HasSelectOrTake
        ? { orderBy: UserGroupByArgs['orderBy'] }
        : { orderBy?: UserGroupByArgs['orderBy'] },
      OrderFields extends ExcludeUnderscoreKeys<Keys<MaybeTupleToUnion<T['orderBy']>>>,
      ByFields extends MaybeTupleToUnion<T['by']>,
      ByValid extends Has<ByFields, OrderFields>,
      HavingFields extends GetHavingFields<T['having']>,
      HavingValid extends Has<ByFields, HavingFields>,
      ByEmpty extends T['by'] extends never[] ? True : False,
      InputErrors extends ByEmpty extends True
      ? `Error: "by" must not be empty.`
      : HavingValid extends False
      ? {
          [P in HavingFields]: P extends ByFields
            ? never
            : P extends string
            ? `Error: Field "${P}" used in "having" needs to be provided in "by".`
            : [
                Error,
                'Field ',
                P,
                ` in "having" needs to be provided in "by"`,
              ]
        }[HavingFields]
      : 'take' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "take", you also need to provide "orderBy"'
      : 'skip' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "skip", you also need to provide "orderBy"'
      : ByValid extends True
      ? {}
      : {
          [P in OrderFields]: P extends ByFields
            ? never
            : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
        }[OrderFields]
    >(args: SubsetIntersection<T, UserGroupByArgs, OrderByArg> & InputErrors): {} extends InputErrors ? GetUserGroupByPayload<T> : Prisma.PrismaPromise<InputErrors>
  /**
   * Fields of the User model
   */
  readonly fields: UserFieldRefs;
  }

  /**
   * The delegate class that acts as a "Promise-like" for User.
   * Why is this prefixed with `Prisma__`?
   * Because we want to prevent naming conflicts as mentioned in
   * https://github.com/prisma/prisma-client-js/issues/707
   */
  export interface Prisma__UserClient<T, Null = never, ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs, GlobalOmitOptions = {}> extends Prisma.PrismaPromise<T> {
    readonly [Symbol.toStringTag]: "PrismaPromise"
    events<T extends User$eventsArgs<ExtArgs> = {}>(args?: Subset<T, User$eventsArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$EventPayload<ExtArgs>, T, "findMany", GlobalOmitOptions> | Null>
    /**
     * Attaches callbacks for the resolution and/or rejection of the Promise.
     * @param onfulfilled The callback to execute when the Promise is resolved.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of which ever callback is executed.
     */
    then<TResult1 = T, TResult2 = never>(onfulfilled?: ((value: T) => TResult1 | PromiseLike<TResult1>) | undefined | null, onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | undefined | null): $Utils.JsPromise<TResult1 | TResult2>
    /**
     * Attaches a callback for only the rejection of the Promise.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of the callback.
     */
    catch<TResult = never>(onrejected?: ((reason: any) => TResult | PromiseLike<TResult>) | undefined | null): $Utils.JsPromise<T | TResult>
    /**
     * Attaches a callback that is invoked when the Promise is settled (fulfilled or rejected). The
     * resolved value cannot be modified from the callback.
     * @param onfinally The callback to execute when the Promise is settled (fulfilled or rejected).
     * @returns A Promise for the completion of the callback.
     */
    finally(onfinally?: (() => void) | undefined | null): $Utils.JsPromise<T>
  }




  /**
   * Fields of the User model
   */
  interface UserFieldRefs {
    readonly id: FieldRef<"User", 'Int'>
    readonly first_name: FieldRef<"User", 'String'>
    readonly last_name: FieldRef<"User", 'String'>
    readonly company_name: FieldRef<"User", 'String'>
    readonly email: FieldRef<"User", 'String'>
    readonly password_hash: FieldRef<"User", 'String'>
    readonly phone: FieldRef<"User", 'String'>
    readonly is_organizer: FieldRef<"User", 'Boolean'>
    readonly is_sponsor: FieldRef<"User", 'Boolean'>
    readonly is_vendor: FieldRef<"User", 'Boolean'>
    readonly is_admin: FieldRef<"User", 'Boolean'>
    readonly is_active: FieldRef<"User", 'Boolean'>
    readonly created_at: FieldRef<"User", 'DateTime'>
    readonly updated_at: FieldRef<"User", 'DateTime'>
  }
    

  // Custom InputTypes
  /**
   * User findUnique
   */
  export type UserFindUniqueArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the User
     */
    select?: UserSelect<ExtArgs> | null
    /**
     * Omit specific fields from the User
     */
    omit?: UserOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: UserInclude<ExtArgs> | null
    /**
     * Filter, which User to fetch.
     */
    where: UserWhereUniqueInput
  }

  /**
   * User findUniqueOrThrow
   */
  export type UserFindUniqueOrThrowArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the User
     */
    select?: UserSelect<ExtArgs> | null
    /**
     * Omit specific fields from the User
     */
    omit?: UserOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: UserInclude<ExtArgs> | null
    /**
     * Filter, which User to fetch.
     */
    where: UserWhereUniqueInput
  }

  /**
   * User findFirst
   */
  export type UserFindFirstArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the User
     */
    select?: UserSelect<ExtArgs> | null
    /**
     * Omit specific fields from the User
     */
    omit?: UserOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: UserInclude<ExtArgs> | null
    /**
     * Filter, which User to fetch.
     */
    where?: UserWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Users to fetch.
     */
    orderBy?: UserOrderByWithRelationInput | UserOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for Users.
     */
    cursor?: UserWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Users from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Users.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of Users.
     */
    distinct?: UserScalarFieldEnum | UserScalarFieldEnum[]
  }

  /**
   * User findFirstOrThrow
   */
  export type UserFindFirstOrThrowArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the User
     */
    select?: UserSelect<ExtArgs> | null
    /**
     * Omit specific fields from the User
     */
    omit?: UserOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: UserInclude<ExtArgs> | null
    /**
     * Filter, which User to fetch.
     */
    where?: UserWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Users to fetch.
     */
    orderBy?: UserOrderByWithRelationInput | UserOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for Users.
     */
    cursor?: UserWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Users from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Users.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of Users.
     */
    distinct?: UserScalarFieldEnum | UserScalarFieldEnum[]
  }

  /**
   * User findMany
   */
  export type UserFindManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the User
     */
    select?: UserSelect<ExtArgs> | null
    /**
     * Omit specific fields from the User
     */
    omit?: UserOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: UserInclude<ExtArgs> | null
    /**
     * Filter, which Users to fetch.
     */
    where?: UserWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Users to fetch.
     */
    orderBy?: UserOrderByWithRelationInput | UserOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for listing Users.
     */
    cursor?: UserWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Users from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Users.
     */
    skip?: number
    distinct?: UserScalarFieldEnum | UserScalarFieldEnum[]
  }

  /**
   * User create
   */
  export type UserCreateArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the User
     */
    select?: UserSelect<ExtArgs> | null
    /**
     * Omit specific fields from the User
     */
    omit?: UserOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: UserInclude<ExtArgs> | null
    /**
     * The data needed to create a User.
     */
    data: XOR<UserCreateInput, UserUncheckedCreateInput>
  }

  /**
   * User createMany
   */
  export type UserCreateManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * The data used to create many Users.
     */
    data: UserCreateManyInput | UserCreateManyInput[]
    skipDuplicates?: boolean
  }

  /**
   * User createManyAndReturn
   */
  export type UserCreateManyAndReturnArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the User
     */
    select?: UserSelectCreateManyAndReturn<ExtArgs> | null
    /**
     * Omit specific fields from the User
     */
    omit?: UserOmit<ExtArgs> | null
    /**
     * The data used to create many Users.
     */
    data: UserCreateManyInput | UserCreateManyInput[]
    skipDuplicates?: boolean
  }

  /**
   * User update
   */
  export type UserUpdateArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the User
     */
    select?: UserSelect<ExtArgs> | null
    /**
     * Omit specific fields from the User
     */
    omit?: UserOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: UserInclude<ExtArgs> | null
    /**
     * The data needed to update a User.
     */
    data: XOR<UserUpdateInput, UserUncheckedUpdateInput>
    /**
     * Choose, which User to update.
     */
    where: UserWhereUniqueInput
  }

  /**
   * User updateMany
   */
  export type UserUpdateManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * The data used to update Users.
     */
    data: XOR<UserUpdateManyMutationInput, UserUncheckedUpdateManyInput>
    /**
     * Filter which Users to update
     */
    where?: UserWhereInput
    /**
     * Limit how many Users to update.
     */
    limit?: number
  }

  /**
   * User updateManyAndReturn
   */
  export type UserUpdateManyAndReturnArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the User
     */
    select?: UserSelectUpdateManyAndReturn<ExtArgs> | null
    /**
     * Omit specific fields from the User
     */
    omit?: UserOmit<ExtArgs> | null
    /**
     * The data used to update Users.
     */
    data: XOR<UserUpdateManyMutationInput, UserUncheckedUpdateManyInput>
    /**
     * Filter which Users to update
     */
    where?: UserWhereInput
    /**
     * Limit how many Users to update.
     */
    limit?: number
  }

  /**
   * User upsert
   */
  export type UserUpsertArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the User
     */
    select?: UserSelect<ExtArgs> | null
    /**
     * Omit specific fields from the User
     */
    omit?: UserOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: UserInclude<ExtArgs> | null
    /**
     * The filter to search for the User to update in case it exists.
     */
    where: UserWhereUniqueInput
    /**
     * In case the User found by the `where` argument doesn't exist, create a new User with this data.
     */
    create: XOR<UserCreateInput, UserUncheckedCreateInput>
    /**
     * In case the User was found with the provided `where` argument, update it with this data.
     */
    update: XOR<UserUpdateInput, UserUncheckedUpdateInput>
  }

  /**
   * User delete
   */
  export type UserDeleteArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the User
     */
    select?: UserSelect<ExtArgs> | null
    /**
     * Omit specific fields from the User
     */
    omit?: UserOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: UserInclude<ExtArgs> | null
    /**
     * Filter which User to delete.
     */
    where: UserWhereUniqueInput
  }

  /**
   * User deleteMany
   */
  export type UserDeleteManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Filter which Users to delete
     */
    where?: UserWhereInput
    /**
     * Limit how many Users to delete.
     */
    limit?: number
  }

  /**
   * User.events
   */
  export type User$eventsArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Event
     */
    select?: EventSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Event
     */
    omit?: EventOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: EventInclude<ExtArgs> | null
    where?: EventWhereInput
    orderBy?: EventOrderByWithRelationInput | EventOrderByWithRelationInput[]
    cursor?: EventWhereUniqueInput
    take?: number
    skip?: number
    distinct?: EventScalarFieldEnum | EventScalarFieldEnum[]
  }

  /**
   * User without action
   */
  export type UserDefaultArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the User
     */
    select?: UserSelect<ExtArgs> | null
    /**
     * Omit specific fields from the User
     */
    omit?: UserOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: UserInclude<ExtArgs> | null
  }


  /**
   * Model Venue
   */

  export type AggregateVenue = {
    _count: VenueCountAggregateOutputType | null
    _avg: VenueAvgAggregateOutputType | null
    _sum: VenueSumAggregateOutputType | null
    _min: VenueMinAggregateOutputType | null
    _max: VenueMaxAggregateOutputType | null
  }

  export type VenueAvgAggregateOutputType = {
    id: number | null
    latitude: number | null
    longitude: number | null
    capacity: number | null
    venue_type_id: number | null
  }

  export type VenueSumAggregateOutputType = {
    id: number | null
    latitude: number | null
    longitude: number | null
    capacity: number | null
    venue_type_id: number | null
  }

  export type VenueMinAggregateOutputType = {
    id: number | null
    name: string | null
    address: string | null
    city: string | null
    state: string | null
    zip_code: string | null
    latitude: number | null
    longitude: number | null
    capacity: number | null
    venue_type_id: number | null
    created_at: Date | null
    updated_at: Date | null
  }

  export type VenueMaxAggregateOutputType = {
    id: number | null
    name: string | null
    address: string | null
    city: string | null
    state: string | null
    zip_code: string | null
    latitude: number | null
    longitude: number | null
    capacity: number | null
    venue_type_id: number | null
    created_at: Date | null
    updated_at: Date | null
  }

  export type VenueCountAggregateOutputType = {
    id: number
    name: number
    address: number
    city: number
    state: number
    zip_code: number
    latitude: number
    longitude: number
    capacity: number
    venue_type_id: number
    created_at: number
    updated_at: number
    _all: number
  }


  export type VenueAvgAggregateInputType = {
    id?: true
    latitude?: true
    longitude?: true
    capacity?: true
    venue_type_id?: true
  }

  export type VenueSumAggregateInputType = {
    id?: true
    latitude?: true
    longitude?: true
    capacity?: true
    venue_type_id?: true
  }

  export type VenueMinAggregateInputType = {
    id?: true
    name?: true
    address?: true
    city?: true
    state?: true
    zip_code?: true
    latitude?: true
    longitude?: true
    capacity?: true
    venue_type_id?: true
    created_at?: true
    updated_at?: true
  }

  export type VenueMaxAggregateInputType = {
    id?: true
    name?: true
    address?: true
    city?: true
    state?: true
    zip_code?: true
    latitude?: true
    longitude?: true
    capacity?: true
    venue_type_id?: true
    created_at?: true
    updated_at?: true
  }

  export type VenueCountAggregateInputType = {
    id?: true
    name?: true
    address?: true
    city?: true
    state?: true
    zip_code?: true
    latitude?: true
    longitude?: true
    capacity?: true
    venue_type_id?: true
    created_at?: true
    updated_at?: true
    _all?: true
  }

  export type VenueAggregateArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Filter which Venue to aggregate.
     */
    where?: VenueWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Venues to fetch.
     */
    orderBy?: VenueOrderByWithRelationInput | VenueOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the start position
     */
    cursor?: VenueWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Venues from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Venues.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Count returned Venues
    **/
    _count?: true | VenueCountAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to average
    **/
    _avg?: VenueAvgAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to sum
    **/
    _sum?: VenueSumAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the minimum value
    **/
    _min?: VenueMinAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the maximum value
    **/
    _max?: VenueMaxAggregateInputType
  }

  export type GetVenueAggregateType<T extends VenueAggregateArgs> = {
        [P in keyof T & keyof AggregateVenue]: P extends '_count' | 'count'
      ? T[P] extends true
        ? number
        : GetScalarType<T[P], AggregateVenue[P]>
      : GetScalarType<T[P], AggregateVenue[P]>
  }




  export type VenueGroupByArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    where?: VenueWhereInput
    orderBy?: VenueOrderByWithAggregationInput | VenueOrderByWithAggregationInput[]
    by: VenueScalarFieldEnum[] | VenueScalarFieldEnum
    having?: VenueScalarWhereWithAggregatesInput
    take?: number
    skip?: number
    _count?: VenueCountAggregateInputType | true
    _avg?: VenueAvgAggregateInputType
    _sum?: VenueSumAggregateInputType
    _min?: VenueMinAggregateInputType
    _max?: VenueMaxAggregateInputType
  }

  export type VenueGroupByOutputType = {
    id: number
    name: string | null
    address: string | null
    city: string | null
    state: string | null
    zip_code: string | null
    latitude: number | null
    longitude: number | null
    capacity: number | null
    venue_type_id: number | null
    created_at: Date | null
    updated_at: Date | null
    _count: VenueCountAggregateOutputType | null
    _avg: VenueAvgAggregateOutputType | null
    _sum: VenueSumAggregateOutputType | null
    _min: VenueMinAggregateOutputType | null
    _max: VenueMaxAggregateOutputType | null
  }

  type GetVenueGroupByPayload<T extends VenueGroupByArgs> = Prisma.PrismaPromise<
    Array<
      PickEnumerable<VenueGroupByOutputType, T['by']> &
        {
          [P in ((keyof T) & (keyof VenueGroupByOutputType))]: P extends '_count'
            ? T[P] extends boolean
              ? number
              : GetScalarType<T[P], VenueGroupByOutputType[P]>
            : GetScalarType<T[P], VenueGroupByOutputType[P]>
        }
      >
    >


  export type VenueSelect<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetSelect<{
    id?: boolean
    name?: boolean
    address?: boolean
    city?: boolean
    state?: boolean
    zip_code?: boolean
    latitude?: boolean
    longitude?: boolean
    capacity?: boolean
    venue_type_id?: boolean
    created_at?: boolean
    updated_at?: boolean
    events?: boolean | Venue$eventsArgs<ExtArgs>
    _count?: boolean | VenueCountOutputTypeDefaultArgs<ExtArgs>
  }, ExtArgs["result"]["venue"]>

  export type VenueSelectCreateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetSelect<{
    id?: boolean
    name?: boolean
    address?: boolean
    city?: boolean
    state?: boolean
    zip_code?: boolean
    latitude?: boolean
    longitude?: boolean
    capacity?: boolean
    venue_type_id?: boolean
    created_at?: boolean
    updated_at?: boolean
  }, ExtArgs["result"]["venue"]>

  export type VenueSelectUpdateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetSelect<{
    id?: boolean
    name?: boolean
    address?: boolean
    city?: boolean
    state?: boolean
    zip_code?: boolean
    latitude?: boolean
    longitude?: boolean
    capacity?: boolean
    venue_type_id?: boolean
    created_at?: boolean
    updated_at?: boolean
  }, ExtArgs["result"]["venue"]>

  export type VenueSelectScalar = {
    id?: boolean
    name?: boolean
    address?: boolean
    city?: boolean
    state?: boolean
    zip_code?: boolean
    latitude?: boolean
    longitude?: boolean
    capacity?: boolean
    venue_type_id?: boolean
    created_at?: boolean
    updated_at?: boolean
  }

  export type VenueOmit<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetOmit<"id" | "name" | "address" | "city" | "state" | "zip_code" | "latitude" | "longitude" | "capacity" | "venue_type_id" | "created_at" | "updated_at", ExtArgs["result"]["venue"]>
  export type VenueInclude<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    events?: boolean | Venue$eventsArgs<ExtArgs>
    _count?: boolean | VenueCountOutputTypeDefaultArgs<ExtArgs>
  }
  export type VenueIncludeCreateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {}
  export type VenueIncludeUpdateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {}

  export type $VenuePayload<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    name: "Venue"
    objects: {
      events: Prisma.$EventPayload<ExtArgs>[]
    }
    scalars: $Extensions.GetPayloadResult<{
      id: number
      name: string | null
      address: string | null
      city: string | null
      state: string | null
      zip_code: string | null
      latitude: number | null
      longitude: number | null
      capacity: number | null
      venue_type_id: number | null
      created_at: Date | null
      updated_at: Date | null
    }, ExtArgs["result"]["venue"]>
    composites: {}
  }

  type VenueGetPayload<S extends boolean | null | undefined | VenueDefaultArgs> = $Result.GetResult<Prisma.$VenuePayload, S>

  type VenueCountArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> =
    Omit<VenueFindManyArgs, 'select' | 'include' | 'distinct' | 'omit'> & {
      select?: VenueCountAggregateInputType | true
    }

  export interface VenueDelegate<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs, GlobalOmitOptions = {}> {
    [K: symbol]: { types: Prisma.TypeMap<ExtArgs>['model']['Venue'], meta: { name: 'Venue' } }
    /**
     * Find zero or one Venue that matches the filter.
     * @param {VenueFindUniqueArgs} args - Arguments to find a Venue
     * @example
     * // Get one Venue
     * const venue = await prisma.venue.findUnique({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findUnique<T extends VenueFindUniqueArgs>(args: SelectSubset<T, VenueFindUniqueArgs<ExtArgs>>): Prisma__VenueClient<$Result.GetResult<Prisma.$VenuePayload<ExtArgs>, T, "findUnique", GlobalOmitOptions> | null, null, ExtArgs, GlobalOmitOptions>

    /**
     * Find one Venue that matches the filter or throw an error with `error.code='P2025'`
     * if no matches were found.
     * @param {VenueFindUniqueOrThrowArgs} args - Arguments to find a Venue
     * @example
     * // Get one Venue
     * const venue = await prisma.venue.findUniqueOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findUniqueOrThrow<T extends VenueFindUniqueOrThrowArgs>(args: SelectSubset<T, VenueFindUniqueOrThrowArgs<ExtArgs>>): Prisma__VenueClient<$Result.GetResult<Prisma.$VenuePayload<ExtArgs>, T, "findUniqueOrThrow", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Find the first Venue that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {VenueFindFirstArgs} args - Arguments to find a Venue
     * @example
     * // Get one Venue
     * const venue = await prisma.venue.findFirst({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findFirst<T extends VenueFindFirstArgs>(args?: SelectSubset<T, VenueFindFirstArgs<ExtArgs>>): Prisma__VenueClient<$Result.GetResult<Prisma.$VenuePayload<ExtArgs>, T, "findFirst", GlobalOmitOptions> | null, null, ExtArgs, GlobalOmitOptions>

    /**
     * Find the first Venue that matches the filter or
     * throw `PrismaKnownClientError` with `P2025` code if no matches were found.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {VenueFindFirstOrThrowArgs} args - Arguments to find a Venue
     * @example
     * // Get one Venue
     * const venue = await prisma.venue.findFirstOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findFirstOrThrow<T extends VenueFindFirstOrThrowArgs>(args?: SelectSubset<T, VenueFindFirstOrThrowArgs<ExtArgs>>): Prisma__VenueClient<$Result.GetResult<Prisma.$VenuePayload<ExtArgs>, T, "findFirstOrThrow", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Find zero or more Venues that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {VenueFindManyArgs} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all Venues
     * const venues = await prisma.venue.findMany()
     * 
     * // Get first 10 Venues
     * const venues = await prisma.venue.findMany({ take: 10 })
     * 
     * // Only select the `id`
     * const venueWithIdOnly = await prisma.venue.findMany({ select: { id: true } })
     * 
     */
    findMany<T extends VenueFindManyArgs>(args?: SelectSubset<T, VenueFindManyArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$VenuePayload<ExtArgs>, T, "findMany", GlobalOmitOptions>>

    /**
     * Create a Venue.
     * @param {VenueCreateArgs} args - Arguments to create a Venue.
     * @example
     * // Create one Venue
     * const Venue = await prisma.venue.create({
     *   data: {
     *     // ... data to create a Venue
     *   }
     * })
     * 
     */
    create<T extends VenueCreateArgs>(args: SelectSubset<T, VenueCreateArgs<ExtArgs>>): Prisma__VenueClient<$Result.GetResult<Prisma.$VenuePayload<ExtArgs>, T, "create", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Create many Venues.
     * @param {VenueCreateManyArgs} args - Arguments to create many Venues.
     * @example
     * // Create many Venues
     * const venue = await prisma.venue.createMany({
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     *     
     */
    createMany<T extends VenueCreateManyArgs>(args?: SelectSubset<T, VenueCreateManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>

    /**
     * Create many Venues and returns the data saved in the database.
     * @param {VenueCreateManyAndReturnArgs} args - Arguments to create many Venues.
     * @example
     * // Create many Venues
     * const venue = await prisma.venue.createManyAndReturn({
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * 
     * // Create many Venues and only return the `id`
     * const venueWithIdOnly = await prisma.venue.createManyAndReturn({
     *   select: { id: true },
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * 
     */
    createManyAndReturn<T extends VenueCreateManyAndReturnArgs>(args?: SelectSubset<T, VenueCreateManyAndReturnArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$VenuePayload<ExtArgs>, T, "createManyAndReturn", GlobalOmitOptions>>

    /**
     * Delete a Venue.
     * @param {VenueDeleteArgs} args - Arguments to delete one Venue.
     * @example
     * // Delete one Venue
     * const Venue = await prisma.venue.delete({
     *   where: {
     *     // ... filter to delete one Venue
     *   }
     * })
     * 
     */
    delete<T extends VenueDeleteArgs>(args: SelectSubset<T, VenueDeleteArgs<ExtArgs>>): Prisma__VenueClient<$Result.GetResult<Prisma.$VenuePayload<ExtArgs>, T, "delete", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Update one Venue.
     * @param {VenueUpdateArgs} args - Arguments to update one Venue.
     * @example
     * // Update one Venue
     * const venue = await prisma.venue.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    update<T extends VenueUpdateArgs>(args: SelectSubset<T, VenueUpdateArgs<ExtArgs>>): Prisma__VenueClient<$Result.GetResult<Prisma.$VenuePayload<ExtArgs>, T, "update", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Delete zero or more Venues.
     * @param {VenueDeleteManyArgs} args - Arguments to filter Venues to delete.
     * @example
     * // Delete a few Venues
     * const { count } = await prisma.venue.deleteMany({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     * 
     */
    deleteMany<T extends VenueDeleteManyArgs>(args?: SelectSubset<T, VenueDeleteManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>

    /**
     * Update zero or more Venues.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {VenueUpdateManyArgs} args - Arguments to update one or more rows.
     * @example
     * // Update many Venues
     * const venue = await prisma.venue.updateMany({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    updateMany<T extends VenueUpdateManyArgs>(args: SelectSubset<T, VenueUpdateManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>

    /**
     * Update zero or more Venues and returns the data updated in the database.
     * @param {VenueUpdateManyAndReturnArgs} args - Arguments to update many Venues.
     * @example
     * // Update many Venues
     * const venue = await prisma.venue.updateManyAndReturn({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * 
     * // Update zero or more Venues and only return the `id`
     * const venueWithIdOnly = await prisma.venue.updateManyAndReturn({
     *   select: { id: true },
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * 
     */
    updateManyAndReturn<T extends VenueUpdateManyAndReturnArgs>(args: SelectSubset<T, VenueUpdateManyAndReturnArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$VenuePayload<ExtArgs>, T, "updateManyAndReturn", GlobalOmitOptions>>

    /**
     * Create or update one Venue.
     * @param {VenueUpsertArgs} args - Arguments to update or create a Venue.
     * @example
     * // Update or create a Venue
     * const venue = await prisma.venue.upsert({
     *   create: {
     *     // ... data to create a Venue
     *   },
     *   update: {
     *     // ... in case it already exists, update
     *   },
     *   where: {
     *     // ... the filter for the Venue we want to update
     *   }
     * })
     */
    upsert<T extends VenueUpsertArgs>(args: SelectSubset<T, VenueUpsertArgs<ExtArgs>>): Prisma__VenueClient<$Result.GetResult<Prisma.$VenuePayload<ExtArgs>, T, "upsert", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>


    /**
     * Count the number of Venues.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {VenueCountArgs} args - Arguments to filter Venues to count.
     * @example
     * // Count the number of Venues
     * const count = await prisma.venue.count({
     *   where: {
     *     // ... the filter for the Venues we want to count
     *   }
     * })
    **/
    count<T extends VenueCountArgs>(
      args?: Subset<T, VenueCountArgs>,
    ): Prisma.PrismaPromise<
      T extends $Utils.Record<'select', any>
        ? T['select'] extends true
          ? number
          : GetScalarType<T['select'], VenueCountAggregateOutputType>
        : number
    >

    /**
     * Allows you to perform aggregations operations on a Venue.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {VenueAggregateArgs} args - Select which aggregations you would like to apply and on what fields.
     * @example
     * // Ordered by age ascending
     * // Where email contains prisma.io
     * // Limited to the 10 users
     * const aggregations = await prisma.user.aggregate({
     *   _avg: {
     *     age: true,
     *   },
     *   where: {
     *     email: {
     *       contains: "prisma.io",
     *     },
     *   },
     *   orderBy: {
     *     age: "asc",
     *   },
     *   take: 10,
     * })
    **/
    aggregate<T extends VenueAggregateArgs>(args: Subset<T, VenueAggregateArgs>): Prisma.PrismaPromise<GetVenueAggregateType<T>>

    /**
     * Group by Venue.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {VenueGroupByArgs} args - Group by arguments.
     * @example
     * // Group by city, order by createdAt, get count
     * const result = await prisma.user.groupBy({
     *   by: ['city', 'createdAt'],
     *   orderBy: {
     *     createdAt: true
     *   },
     *   _count: {
     *     _all: true
     *   },
     * })
     * 
    **/
    groupBy<
      T extends VenueGroupByArgs,
      HasSelectOrTake extends Or<
        Extends<'skip', Keys<T>>,
        Extends<'take', Keys<T>>
      >,
      OrderByArg extends True extends HasSelectOrTake
        ? { orderBy: VenueGroupByArgs['orderBy'] }
        : { orderBy?: VenueGroupByArgs['orderBy'] },
      OrderFields extends ExcludeUnderscoreKeys<Keys<MaybeTupleToUnion<T['orderBy']>>>,
      ByFields extends MaybeTupleToUnion<T['by']>,
      ByValid extends Has<ByFields, OrderFields>,
      HavingFields extends GetHavingFields<T['having']>,
      HavingValid extends Has<ByFields, HavingFields>,
      ByEmpty extends T['by'] extends never[] ? True : False,
      InputErrors extends ByEmpty extends True
      ? `Error: "by" must not be empty.`
      : HavingValid extends False
      ? {
          [P in HavingFields]: P extends ByFields
            ? never
            : P extends string
            ? `Error: Field "${P}" used in "having" needs to be provided in "by".`
            : [
                Error,
                'Field ',
                P,
                ` in "having" needs to be provided in "by"`,
              ]
        }[HavingFields]
      : 'take' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "take", you also need to provide "orderBy"'
      : 'skip' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "skip", you also need to provide "orderBy"'
      : ByValid extends True
      ? {}
      : {
          [P in OrderFields]: P extends ByFields
            ? never
            : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
        }[OrderFields]
    >(args: SubsetIntersection<T, VenueGroupByArgs, OrderByArg> & InputErrors): {} extends InputErrors ? GetVenueGroupByPayload<T> : Prisma.PrismaPromise<InputErrors>
  /**
   * Fields of the Venue model
   */
  readonly fields: VenueFieldRefs;
  }

  /**
   * The delegate class that acts as a "Promise-like" for Venue.
   * Why is this prefixed with `Prisma__`?
   * Because we want to prevent naming conflicts as mentioned in
   * https://github.com/prisma/prisma-client-js/issues/707
   */
  export interface Prisma__VenueClient<T, Null = never, ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs, GlobalOmitOptions = {}> extends Prisma.PrismaPromise<T> {
    readonly [Symbol.toStringTag]: "PrismaPromise"
    events<T extends Venue$eventsArgs<ExtArgs> = {}>(args?: Subset<T, Venue$eventsArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$EventPayload<ExtArgs>, T, "findMany", GlobalOmitOptions> | Null>
    /**
     * Attaches callbacks for the resolution and/or rejection of the Promise.
     * @param onfulfilled The callback to execute when the Promise is resolved.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of which ever callback is executed.
     */
    then<TResult1 = T, TResult2 = never>(onfulfilled?: ((value: T) => TResult1 | PromiseLike<TResult1>) | undefined | null, onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | undefined | null): $Utils.JsPromise<TResult1 | TResult2>
    /**
     * Attaches a callback for only the rejection of the Promise.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of the callback.
     */
    catch<TResult = never>(onrejected?: ((reason: any) => TResult | PromiseLike<TResult>) | undefined | null): $Utils.JsPromise<T | TResult>
    /**
     * Attaches a callback that is invoked when the Promise is settled (fulfilled or rejected). The
     * resolved value cannot be modified from the callback.
     * @param onfinally The callback to execute when the Promise is settled (fulfilled or rejected).
     * @returns A Promise for the completion of the callback.
     */
    finally(onfinally?: (() => void) | undefined | null): $Utils.JsPromise<T>
  }




  /**
   * Fields of the Venue model
   */
  interface VenueFieldRefs {
    readonly id: FieldRef<"Venue", 'Int'>
    readonly name: FieldRef<"Venue", 'String'>
    readonly address: FieldRef<"Venue", 'String'>
    readonly city: FieldRef<"Venue", 'String'>
    readonly state: FieldRef<"Venue", 'String'>
    readonly zip_code: FieldRef<"Venue", 'String'>
    readonly latitude: FieldRef<"Venue", 'Float'>
    readonly longitude: FieldRef<"Venue", 'Float'>
    readonly capacity: FieldRef<"Venue", 'Int'>
    readonly venue_type_id: FieldRef<"Venue", 'Int'>
    readonly created_at: FieldRef<"Venue", 'DateTime'>
    readonly updated_at: FieldRef<"Venue", 'DateTime'>
  }
    

  // Custom InputTypes
  /**
   * Venue findUnique
   */
  export type VenueFindUniqueArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Venue
     */
    select?: VenueSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Venue
     */
    omit?: VenueOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: VenueInclude<ExtArgs> | null
    /**
     * Filter, which Venue to fetch.
     */
    where: VenueWhereUniqueInput
  }

  /**
   * Venue findUniqueOrThrow
   */
  export type VenueFindUniqueOrThrowArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Venue
     */
    select?: VenueSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Venue
     */
    omit?: VenueOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: VenueInclude<ExtArgs> | null
    /**
     * Filter, which Venue to fetch.
     */
    where: VenueWhereUniqueInput
  }

  /**
   * Venue findFirst
   */
  export type VenueFindFirstArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Venue
     */
    select?: VenueSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Venue
     */
    omit?: VenueOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: VenueInclude<ExtArgs> | null
    /**
     * Filter, which Venue to fetch.
     */
    where?: VenueWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Venues to fetch.
     */
    orderBy?: VenueOrderByWithRelationInput | VenueOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for Venues.
     */
    cursor?: VenueWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Venues from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Venues.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of Venues.
     */
    distinct?: VenueScalarFieldEnum | VenueScalarFieldEnum[]
  }

  /**
   * Venue findFirstOrThrow
   */
  export type VenueFindFirstOrThrowArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Venue
     */
    select?: VenueSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Venue
     */
    omit?: VenueOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: VenueInclude<ExtArgs> | null
    /**
     * Filter, which Venue to fetch.
     */
    where?: VenueWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Venues to fetch.
     */
    orderBy?: VenueOrderByWithRelationInput | VenueOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for Venues.
     */
    cursor?: VenueWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Venues from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Venues.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of Venues.
     */
    distinct?: VenueScalarFieldEnum | VenueScalarFieldEnum[]
  }

  /**
   * Venue findMany
   */
  export type VenueFindManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Venue
     */
    select?: VenueSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Venue
     */
    omit?: VenueOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: VenueInclude<ExtArgs> | null
    /**
     * Filter, which Venues to fetch.
     */
    where?: VenueWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of Venues to fetch.
     */
    orderBy?: VenueOrderByWithRelationInput | VenueOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for listing Venues.
     */
    cursor?: VenueWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` Venues from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` Venues.
     */
    skip?: number
    distinct?: VenueScalarFieldEnum | VenueScalarFieldEnum[]
  }

  /**
   * Venue create
   */
  export type VenueCreateArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Venue
     */
    select?: VenueSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Venue
     */
    omit?: VenueOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: VenueInclude<ExtArgs> | null
    /**
     * The data needed to create a Venue.
     */
    data?: XOR<VenueCreateInput, VenueUncheckedCreateInput>
  }

  /**
   * Venue createMany
   */
  export type VenueCreateManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * The data used to create many Venues.
     */
    data: VenueCreateManyInput | VenueCreateManyInput[]
    skipDuplicates?: boolean
  }

  /**
   * Venue createManyAndReturn
   */
  export type VenueCreateManyAndReturnArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Venue
     */
    select?: VenueSelectCreateManyAndReturn<ExtArgs> | null
    /**
     * Omit specific fields from the Venue
     */
    omit?: VenueOmit<ExtArgs> | null
    /**
     * The data used to create many Venues.
     */
    data: VenueCreateManyInput | VenueCreateManyInput[]
    skipDuplicates?: boolean
  }

  /**
   * Venue update
   */
  export type VenueUpdateArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Venue
     */
    select?: VenueSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Venue
     */
    omit?: VenueOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: VenueInclude<ExtArgs> | null
    /**
     * The data needed to update a Venue.
     */
    data: XOR<VenueUpdateInput, VenueUncheckedUpdateInput>
    /**
     * Choose, which Venue to update.
     */
    where: VenueWhereUniqueInput
  }

  /**
   * Venue updateMany
   */
  export type VenueUpdateManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * The data used to update Venues.
     */
    data: XOR<VenueUpdateManyMutationInput, VenueUncheckedUpdateManyInput>
    /**
     * Filter which Venues to update
     */
    where?: VenueWhereInput
    /**
     * Limit how many Venues to update.
     */
    limit?: number
  }

  /**
   * Venue updateManyAndReturn
   */
  export type VenueUpdateManyAndReturnArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Venue
     */
    select?: VenueSelectUpdateManyAndReturn<ExtArgs> | null
    /**
     * Omit specific fields from the Venue
     */
    omit?: VenueOmit<ExtArgs> | null
    /**
     * The data used to update Venues.
     */
    data: XOR<VenueUpdateManyMutationInput, VenueUncheckedUpdateManyInput>
    /**
     * Filter which Venues to update
     */
    where?: VenueWhereInput
    /**
     * Limit how many Venues to update.
     */
    limit?: number
  }

  /**
   * Venue upsert
   */
  export type VenueUpsertArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Venue
     */
    select?: VenueSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Venue
     */
    omit?: VenueOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: VenueInclude<ExtArgs> | null
    /**
     * The filter to search for the Venue to update in case it exists.
     */
    where: VenueWhereUniqueInput
    /**
     * In case the Venue found by the `where` argument doesn't exist, create a new Venue with this data.
     */
    create: XOR<VenueCreateInput, VenueUncheckedCreateInput>
    /**
     * In case the Venue was found with the provided `where` argument, update it with this data.
     */
    update: XOR<VenueUpdateInput, VenueUncheckedUpdateInput>
  }

  /**
   * Venue delete
   */
  export type VenueDeleteArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Venue
     */
    select?: VenueSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Venue
     */
    omit?: VenueOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: VenueInclude<ExtArgs> | null
    /**
     * Filter which Venue to delete.
     */
    where: VenueWhereUniqueInput
  }

  /**
   * Venue deleteMany
   */
  export type VenueDeleteManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Filter which Venues to delete
     */
    where?: VenueWhereInput
    /**
     * Limit how many Venues to delete.
     */
    limit?: number
  }

  /**
   * Venue.events
   */
  export type Venue$eventsArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Event
     */
    select?: EventSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Event
     */
    omit?: EventOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: EventInclude<ExtArgs> | null
    where?: EventWhereInput
    orderBy?: EventOrderByWithRelationInput | EventOrderByWithRelationInput[]
    cursor?: EventWhereUniqueInput
    take?: number
    skip?: number
    distinct?: EventScalarFieldEnum | EventScalarFieldEnum[]
  }

  /**
   * Venue without action
   */
  export type VenueDefaultArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the Venue
     */
    select?: VenueSelect<ExtArgs> | null
    /**
     * Omit specific fields from the Venue
     */
    omit?: VenueOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: VenueInclude<ExtArgs> | null
  }


  /**
   * Model FunalyticsScore
   */

  export type AggregateFunalyticsScore = {
    _count: FunalyticsScoreCountAggregateOutputType | null
    _avg: FunalyticsScoreAvgAggregateOutputType | null
    _sum: FunalyticsScoreSumAggregateOutputType | null
    _min: FunalyticsScoreMinAggregateOutputType | null
    _max: FunalyticsScoreMaxAggregateOutputType | null
  }

  export type FunalyticsScoreAvgAggregateOutputType = {
    eventId: number | null
    communityVibe: number | null
    familyFun: number | null
    overallScore: number | null
  }

  export type FunalyticsScoreSumAggregateOutputType = {
    eventId: number | null
    communityVibe: number | null
    familyFun: number | null
    overallScore: number | null
  }

  export type FunalyticsScoreMinAggregateOutputType = {
    id: string | null
    eventId: number | null
    communityVibe: number | null
    familyFun: number | null
    overallScore: number | null
    reasoning: string | null
    computedAt: Date | null
  }

  export type FunalyticsScoreMaxAggregateOutputType = {
    id: string | null
    eventId: number | null
    communityVibe: number | null
    familyFun: number | null
    overallScore: number | null
    reasoning: string | null
    computedAt: Date | null
  }

  export type FunalyticsScoreCountAggregateOutputType = {
    id: number
    eventId: number
    communityVibe: number
    familyFun: number
    overallScore: number
    reasoning: number
    computedAt: number
    _all: number
  }


  export type FunalyticsScoreAvgAggregateInputType = {
    eventId?: true
    communityVibe?: true
    familyFun?: true
    overallScore?: true
  }

  export type FunalyticsScoreSumAggregateInputType = {
    eventId?: true
    communityVibe?: true
    familyFun?: true
    overallScore?: true
  }

  export type FunalyticsScoreMinAggregateInputType = {
    id?: true
    eventId?: true
    communityVibe?: true
    familyFun?: true
    overallScore?: true
    reasoning?: true
    computedAt?: true
  }

  export type FunalyticsScoreMaxAggregateInputType = {
    id?: true
    eventId?: true
    communityVibe?: true
    familyFun?: true
    overallScore?: true
    reasoning?: true
    computedAt?: true
  }

  export type FunalyticsScoreCountAggregateInputType = {
    id?: true
    eventId?: true
    communityVibe?: true
    familyFun?: true
    overallScore?: true
    reasoning?: true
    computedAt?: true
    _all?: true
  }

  export type FunalyticsScoreAggregateArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Filter which FunalyticsScore to aggregate.
     */
    where?: FunalyticsScoreWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of FunalyticsScores to fetch.
     */
    orderBy?: FunalyticsScoreOrderByWithRelationInput | FunalyticsScoreOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the start position
     */
    cursor?: FunalyticsScoreWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` FunalyticsScores from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` FunalyticsScores.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Count returned FunalyticsScores
    **/
    _count?: true | FunalyticsScoreCountAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to average
    **/
    _avg?: FunalyticsScoreAvgAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to sum
    **/
    _sum?: FunalyticsScoreSumAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the minimum value
    **/
    _min?: FunalyticsScoreMinAggregateInputType
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/aggregations Aggregation Docs}
     * 
     * Select which fields to find the maximum value
    **/
    _max?: FunalyticsScoreMaxAggregateInputType
  }

  export type GetFunalyticsScoreAggregateType<T extends FunalyticsScoreAggregateArgs> = {
        [P in keyof T & keyof AggregateFunalyticsScore]: P extends '_count' | 'count'
      ? T[P] extends true
        ? number
        : GetScalarType<T[P], AggregateFunalyticsScore[P]>
      : GetScalarType<T[P], AggregateFunalyticsScore[P]>
  }




  export type FunalyticsScoreGroupByArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    where?: FunalyticsScoreWhereInput
    orderBy?: FunalyticsScoreOrderByWithAggregationInput | FunalyticsScoreOrderByWithAggregationInput[]
    by: FunalyticsScoreScalarFieldEnum[] | FunalyticsScoreScalarFieldEnum
    having?: FunalyticsScoreScalarWhereWithAggregatesInput
    take?: number
    skip?: number
    _count?: FunalyticsScoreCountAggregateInputType | true
    _avg?: FunalyticsScoreAvgAggregateInputType
    _sum?: FunalyticsScoreSumAggregateInputType
    _min?: FunalyticsScoreMinAggregateInputType
    _max?: FunalyticsScoreMaxAggregateInputType
  }

  export type FunalyticsScoreGroupByOutputType = {
    id: string
    eventId: number
    communityVibe: number | null
    familyFun: number | null
    overallScore: number | null
    reasoning: string | null
    computedAt: Date
    _count: FunalyticsScoreCountAggregateOutputType | null
    _avg: FunalyticsScoreAvgAggregateOutputType | null
    _sum: FunalyticsScoreSumAggregateOutputType | null
    _min: FunalyticsScoreMinAggregateOutputType | null
    _max: FunalyticsScoreMaxAggregateOutputType | null
  }

  type GetFunalyticsScoreGroupByPayload<T extends FunalyticsScoreGroupByArgs> = Prisma.PrismaPromise<
    Array<
      PickEnumerable<FunalyticsScoreGroupByOutputType, T['by']> &
        {
          [P in ((keyof T) & (keyof FunalyticsScoreGroupByOutputType))]: P extends '_count'
            ? T[P] extends boolean
              ? number
              : GetScalarType<T[P], FunalyticsScoreGroupByOutputType[P]>
            : GetScalarType<T[P], FunalyticsScoreGroupByOutputType[P]>
        }
      >
    >


  export type FunalyticsScoreSelect<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetSelect<{
    id?: boolean
    eventId?: boolean
    communityVibe?: boolean
    familyFun?: boolean
    overallScore?: boolean
    reasoning?: boolean
    computedAt?: boolean
    event?: boolean | EventDefaultArgs<ExtArgs>
  }, ExtArgs["result"]["funalyticsScore"]>

  export type FunalyticsScoreSelectCreateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetSelect<{
    id?: boolean
    eventId?: boolean
    communityVibe?: boolean
    familyFun?: boolean
    overallScore?: boolean
    reasoning?: boolean
    computedAt?: boolean
    event?: boolean | EventDefaultArgs<ExtArgs>
  }, ExtArgs["result"]["funalyticsScore"]>

  export type FunalyticsScoreSelectUpdateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetSelect<{
    id?: boolean
    eventId?: boolean
    communityVibe?: boolean
    familyFun?: boolean
    overallScore?: boolean
    reasoning?: boolean
    computedAt?: boolean
    event?: boolean | EventDefaultArgs<ExtArgs>
  }, ExtArgs["result"]["funalyticsScore"]>

  export type FunalyticsScoreSelectScalar = {
    id?: boolean
    eventId?: boolean
    communityVibe?: boolean
    familyFun?: boolean
    overallScore?: boolean
    reasoning?: boolean
    computedAt?: boolean
  }

  export type FunalyticsScoreOmit<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = $Extensions.GetOmit<"id" | "eventId" | "communityVibe" | "familyFun" | "overallScore" | "reasoning" | "computedAt", ExtArgs["result"]["funalyticsScore"]>
  export type FunalyticsScoreInclude<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    event?: boolean | EventDefaultArgs<ExtArgs>
  }
  export type FunalyticsScoreIncludeCreateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    event?: boolean | EventDefaultArgs<ExtArgs>
  }
  export type FunalyticsScoreIncludeUpdateManyAndReturn<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    event?: boolean | EventDefaultArgs<ExtArgs>
  }

  export type $FunalyticsScorePayload<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    name: "FunalyticsScore"
    objects: {
      event: Prisma.$EventPayload<ExtArgs>
    }
    scalars: $Extensions.GetPayloadResult<{
      id: string
      eventId: number
      communityVibe: number | null
      familyFun: number | null
      overallScore: number | null
      reasoning: string | null
      computedAt: Date
    }, ExtArgs["result"]["funalyticsScore"]>
    composites: {}
  }

  type FunalyticsScoreGetPayload<S extends boolean | null | undefined | FunalyticsScoreDefaultArgs> = $Result.GetResult<Prisma.$FunalyticsScorePayload, S>

  type FunalyticsScoreCountArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> =
    Omit<FunalyticsScoreFindManyArgs, 'select' | 'include' | 'distinct' | 'omit'> & {
      select?: FunalyticsScoreCountAggregateInputType | true
    }

  export interface FunalyticsScoreDelegate<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs, GlobalOmitOptions = {}> {
    [K: symbol]: { types: Prisma.TypeMap<ExtArgs>['model']['FunalyticsScore'], meta: { name: 'FunalyticsScore' } }
    /**
     * Find zero or one FunalyticsScore that matches the filter.
     * @param {FunalyticsScoreFindUniqueArgs} args - Arguments to find a FunalyticsScore
     * @example
     * // Get one FunalyticsScore
     * const funalyticsScore = await prisma.funalyticsScore.findUnique({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findUnique<T extends FunalyticsScoreFindUniqueArgs>(args: SelectSubset<T, FunalyticsScoreFindUniqueArgs<ExtArgs>>): Prisma__FunalyticsScoreClient<$Result.GetResult<Prisma.$FunalyticsScorePayload<ExtArgs>, T, "findUnique", GlobalOmitOptions> | null, null, ExtArgs, GlobalOmitOptions>

    /**
     * Find one FunalyticsScore that matches the filter or throw an error with `error.code='P2025'`
     * if no matches were found.
     * @param {FunalyticsScoreFindUniqueOrThrowArgs} args - Arguments to find a FunalyticsScore
     * @example
     * // Get one FunalyticsScore
     * const funalyticsScore = await prisma.funalyticsScore.findUniqueOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findUniqueOrThrow<T extends FunalyticsScoreFindUniqueOrThrowArgs>(args: SelectSubset<T, FunalyticsScoreFindUniqueOrThrowArgs<ExtArgs>>): Prisma__FunalyticsScoreClient<$Result.GetResult<Prisma.$FunalyticsScorePayload<ExtArgs>, T, "findUniqueOrThrow", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Find the first FunalyticsScore that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {FunalyticsScoreFindFirstArgs} args - Arguments to find a FunalyticsScore
     * @example
     * // Get one FunalyticsScore
     * const funalyticsScore = await prisma.funalyticsScore.findFirst({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findFirst<T extends FunalyticsScoreFindFirstArgs>(args?: SelectSubset<T, FunalyticsScoreFindFirstArgs<ExtArgs>>): Prisma__FunalyticsScoreClient<$Result.GetResult<Prisma.$FunalyticsScorePayload<ExtArgs>, T, "findFirst", GlobalOmitOptions> | null, null, ExtArgs, GlobalOmitOptions>

    /**
     * Find the first FunalyticsScore that matches the filter or
     * throw `PrismaKnownClientError` with `P2025` code if no matches were found.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {FunalyticsScoreFindFirstOrThrowArgs} args - Arguments to find a FunalyticsScore
     * @example
     * // Get one FunalyticsScore
     * const funalyticsScore = await prisma.funalyticsScore.findFirstOrThrow({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     */
    findFirstOrThrow<T extends FunalyticsScoreFindFirstOrThrowArgs>(args?: SelectSubset<T, FunalyticsScoreFindFirstOrThrowArgs<ExtArgs>>): Prisma__FunalyticsScoreClient<$Result.GetResult<Prisma.$FunalyticsScorePayload<ExtArgs>, T, "findFirstOrThrow", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Find zero or more FunalyticsScores that matches the filter.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {FunalyticsScoreFindManyArgs} args - Arguments to filter and select certain fields only.
     * @example
     * // Get all FunalyticsScores
     * const funalyticsScores = await prisma.funalyticsScore.findMany()
     * 
     * // Get first 10 FunalyticsScores
     * const funalyticsScores = await prisma.funalyticsScore.findMany({ take: 10 })
     * 
     * // Only select the `id`
     * const funalyticsScoreWithIdOnly = await prisma.funalyticsScore.findMany({ select: { id: true } })
     * 
     */
    findMany<T extends FunalyticsScoreFindManyArgs>(args?: SelectSubset<T, FunalyticsScoreFindManyArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$FunalyticsScorePayload<ExtArgs>, T, "findMany", GlobalOmitOptions>>

    /**
     * Create a FunalyticsScore.
     * @param {FunalyticsScoreCreateArgs} args - Arguments to create a FunalyticsScore.
     * @example
     * // Create one FunalyticsScore
     * const FunalyticsScore = await prisma.funalyticsScore.create({
     *   data: {
     *     // ... data to create a FunalyticsScore
     *   }
     * })
     * 
     */
    create<T extends FunalyticsScoreCreateArgs>(args: SelectSubset<T, FunalyticsScoreCreateArgs<ExtArgs>>): Prisma__FunalyticsScoreClient<$Result.GetResult<Prisma.$FunalyticsScorePayload<ExtArgs>, T, "create", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Create many FunalyticsScores.
     * @param {FunalyticsScoreCreateManyArgs} args - Arguments to create many FunalyticsScores.
     * @example
     * // Create many FunalyticsScores
     * const funalyticsScore = await prisma.funalyticsScore.createMany({
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     *     
     */
    createMany<T extends FunalyticsScoreCreateManyArgs>(args?: SelectSubset<T, FunalyticsScoreCreateManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>

    /**
     * Create many FunalyticsScores and returns the data saved in the database.
     * @param {FunalyticsScoreCreateManyAndReturnArgs} args - Arguments to create many FunalyticsScores.
     * @example
     * // Create many FunalyticsScores
     * const funalyticsScore = await prisma.funalyticsScore.createManyAndReturn({
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * 
     * // Create many FunalyticsScores and only return the `id`
     * const funalyticsScoreWithIdOnly = await prisma.funalyticsScore.createManyAndReturn({
     *   select: { id: true },
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * 
     */
    createManyAndReturn<T extends FunalyticsScoreCreateManyAndReturnArgs>(args?: SelectSubset<T, FunalyticsScoreCreateManyAndReturnArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$FunalyticsScorePayload<ExtArgs>, T, "createManyAndReturn", GlobalOmitOptions>>

    /**
     * Delete a FunalyticsScore.
     * @param {FunalyticsScoreDeleteArgs} args - Arguments to delete one FunalyticsScore.
     * @example
     * // Delete one FunalyticsScore
     * const FunalyticsScore = await prisma.funalyticsScore.delete({
     *   where: {
     *     // ... filter to delete one FunalyticsScore
     *   }
     * })
     * 
     */
    delete<T extends FunalyticsScoreDeleteArgs>(args: SelectSubset<T, FunalyticsScoreDeleteArgs<ExtArgs>>): Prisma__FunalyticsScoreClient<$Result.GetResult<Prisma.$FunalyticsScorePayload<ExtArgs>, T, "delete", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Update one FunalyticsScore.
     * @param {FunalyticsScoreUpdateArgs} args - Arguments to update one FunalyticsScore.
     * @example
     * // Update one FunalyticsScore
     * const funalyticsScore = await prisma.funalyticsScore.update({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    update<T extends FunalyticsScoreUpdateArgs>(args: SelectSubset<T, FunalyticsScoreUpdateArgs<ExtArgs>>): Prisma__FunalyticsScoreClient<$Result.GetResult<Prisma.$FunalyticsScorePayload<ExtArgs>, T, "update", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>

    /**
     * Delete zero or more FunalyticsScores.
     * @param {FunalyticsScoreDeleteManyArgs} args - Arguments to filter FunalyticsScores to delete.
     * @example
     * // Delete a few FunalyticsScores
     * const { count } = await prisma.funalyticsScore.deleteMany({
     *   where: {
     *     // ... provide filter here
     *   }
     * })
     * 
     */
    deleteMany<T extends FunalyticsScoreDeleteManyArgs>(args?: SelectSubset<T, FunalyticsScoreDeleteManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>

    /**
     * Update zero or more FunalyticsScores.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {FunalyticsScoreUpdateManyArgs} args - Arguments to update one or more rows.
     * @example
     * // Update many FunalyticsScores
     * const funalyticsScore = await prisma.funalyticsScore.updateMany({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: {
     *     // ... provide data here
     *   }
     * })
     * 
     */
    updateMany<T extends FunalyticsScoreUpdateManyArgs>(args: SelectSubset<T, FunalyticsScoreUpdateManyArgs<ExtArgs>>): Prisma.PrismaPromise<BatchPayload>

    /**
     * Update zero or more FunalyticsScores and returns the data updated in the database.
     * @param {FunalyticsScoreUpdateManyAndReturnArgs} args - Arguments to update many FunalyticsScores.
     * @example
     * // Update many FunalyticsScores
     * const funalyticsScore = await prisma.funalyticsScore.updateManyAndReturn({
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * 
     * // Update zero or more FunalyticsScores and only return the `id`
     * const funalyticsScoreWithIdOnly = await prisma.funalyticsScore.updateManyAndReturn({
     *   select: { id: true },
     *   where: {
     *     // ... provide filter here
     *   },
     *   data: [
     *     // ... provide data here
     *   ]
     * })
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * 
     */
    updateManyAndReturn<T extends FunalyticsScoreUpdateManyAndReturnArgs>(args: SelectSubset<T, FunalyticsScoreUpdateManyAndReturnArgs<ExtArgs>>): Prisma.PrismaPromise<$Result.GetResult<Prisma.$FunalyticsScorePayload<ExtArgs>, T, "updateManyAndReturn", GlobalOmitOptions>>

    /**
     * Create or update one FunalyticsScore.
     * @param {FunalyticsScoreUpsertArgs} args - Arguments to update or create a FunalyticsScore.
     * @example
     * // Update or create a FunalyticsScore
     * const funalyticsScore = await prisma.funalyticsScore.upsert({
     *   create: {
     *     // ... data to create a FunalyticsScore
     *   },
     *   update: {
     *     // ... in case it already exists, update
     *   },
     *   where: {
     *     // ... the filter for the FunalyticsScore we want to update
     *   }
     * })
     */
    upsert<T extends FunalyticsScoreUpsertArgs>(args: SelectSubset<T, FunalyticsScoreUpsertArgs<ExtArgs>>): Prisma__FunalyticsScoreClient<$Result.GetResult<Prisma.$FunalyticsScorePayload<ExtArgs>, T, "upsert", GlobalOmitOptions>, never, ExtArgs, GlobalOmitOptions>


    /**
     * Count the number of FunalyticsScores.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {FunalyticsScoreCountArgs} args - Arguments to filter FunalyticsScores to count.
     * @example
     * // Count the number of FunalyticsScores
     * const count = await prisma.funalyticsScore.count({
     *   where: {
     *     // ... the filter for the FunalyticsScores we want to count
     *   }
     * })
    **/
    count<T extends FunalyticsScoreCountArgs>(
      args?: Subset<T, FunalyticsScoreCountArgs>,
    ): Prisma.PrismaPromise<
      T extends $Utils.Record<'select', any>
        ? T['select'] extends true
          ? number
          : GetScalarType<T['select'], FunalyticsScoreCountAggregateOutputType>
        : number
    >

    /**
     * Allows you to perform aggregations operations on a FunalyticsScore.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {FunalyticsScoreAggregateArgs} args - Select which aggregations you would like to apply and on what fields.
     * @example
     * // Ordered by age ascending
     * // Where email contains prisma.io
     * // Limited to the 10 users
     * const aggregations = await prisma.user.aggregate({
     *   _avg: {
     *     age: true,
     *   },
     *   where: {
     *     email: {
     *       contains: "prisma.io",
     *     },
     *   },
     *   orderBy: {
     *     age: "asc",
     *   },
     *   take: 10,
     * })
    **/
    aggregate<T extends FunalyticsScoreAggregateArgs>(args: Subset<T, FunalyticsScoreAggregateArgs>): Prisma.PrismaPromise<GetFunalyticsScoreAggregateType<T>>

    /**
     * Group by FunalyticsScore.
     * Note, that providing `undefined` is treated as the value not being there.
     * Read more here: https://pris.ly/d/null-undefined
     * @param {FunalyticsScoreGroupByArgs} args - Group by arguments.
     * @example
     * // Group by city, order by createdAt, get count
     * const result = await prisma.user.groupBy({
     *   by: ['city', 'createdAt'],
     *   orderBy: {
     *     createdAt: true
     *   },
     *   _count: {
     *     _all: true
     *   },
     * })
     * 
    **/
    groupBy<
      T extends FunalyticsScoreGroupByArgs,
      HasSelectOrTake extends Or<
        Extends<'skip', Keys<T>>,
        Extends<'take', Keys<T>>
      >,
      OrderByArg extends True extends HasSelectOrTake
        ? { orderBy: FunalyticsScoreGroupByArgs['orderBy'] }
        : { orderBy?: FunalyticsScoreGroupByArgs['orderBy'] },
      OrderFields extends ExcludeUnderscoreKeys<Keys<MaybeTupleToUnion<T['orderBy']>>>,
      ByFields extends MaybeTupleToUnion<T['by']>,
      ByValid extends Has<ByFields, OrderFields>,
      HavingFields extends GetHavingFields<T['having']>,
      HavingValid extends Has<ByFields, HavingFields>,
      ByEmpty extends T['by'] extends never[] ? True : False,
      InputErrors extends ByEmpty extends True
      ? `Error: "by" must not be empty.`
      : HavingValid extends False
      ? {
          [P in HavingFields]: P extends ByFields
            ? never
            : P extends string
            ? `Error: Field "${P}" used in "having" needs to be provided in "by".`
            : [
                Error,
                'Field ',
                P,
                ` in "having" needs to be provided in "by"`,
              ]
        }[HavingFields]
      : 'take' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "take", you also need to provide "orderBy"'
      : 'skip' extends Keys<T>
      ? 'orderBy' extends Keys<T>
        ? ByValid extends True
          ? {}
          : {
              [P in OrderFields]: P extends ByFields
                ? never
                : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
            }[OrderFields]
        : 'Error: If you provide "skip", you also need to provide "orderBy"'
      : ByValid extends True
      ? {}
      : {
          [P in OrderFields]: P extends ByFields
            ? never
            : `Error: Field "${P}" in "orderBy" needs to be provided in "by"`
        }[OrderFields]
    >(args: SubsetIntersection<T, FunalyticsScoreGroupByArgs, OrderByArg> & InputErrors): {} extends InputErrors ? GetFunalyticsScoreGroupByPayload<T> : Prisma.PrismaPromise<InputErrors>
  /**
   * Fields of the FunalyticsScore model
   */
  readonly fields: FunalyticsScoreFieldRefs;
  }

  /**
   * The delegate class that acts as a "Promise-like" for FunalyticsScore.
   * Why is this prefixed with `Prisma__`?
   * Because we want to prevent naming conflicts as mentioned in
   * https://github.com/prisma/prisma-client-js/issues/707
   */
  export interface Prisma__FunalyticsScoreClient<T, Null = never, ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs, GlobalOmitOptions = {}> extends Prisma.PrismaPromise<T> {
    readonly [Symbol.toStringTag]: "PrismaPromise"
    event<T extends EventDefaultArgs<ExtArgs> = {}>(args?: Subset<T, EventDefaultArgs<ExtArgs>>): Prisma__EventClient<$Result.GetResult<Prisma.$EventPayload<ExtArgs>, T, "findUniqueOrThrow", GlobalOmitOptions> | Null, Null, ExtArgs, GlobalOmitOptions>
    /**
     * Attaches callbacks for the resolution and/or rejection of the Promise.
     * @param onfulfilled The callback to execute when the Promise is resolved.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of which ever callback is executed.
     */
    then<TResult1 = T, TResult2 = never>(onfulfilled?: ((value: T) => TResult1 | PromiseLike<TResult1>) | undefined | null, onrejected?: ((reason: any) => TResult2 | PromiseLike<TResult2>) | undefined | null): $Utils.JsPromise<TResult1 | TResult2>
    /**
     * Attaches a callback for only the rejection of the Promise.
     * @param onrejected The callback to execute when the Promise is rejected.
     * @returns A Promise for the completion of the callback.
     */
    catch<TResult = never>(onrejected?: ((reason: any) => TResult | PromiseLike<TResult>) | undefined | null): $Utils.JsPromise<T | TResult>
    /**
     * Attaches a callback that is invoked when the Promise is settled (fulfilled or rejected). The
     * resolved value cannot be modified from the callback.
     * @param onfinally The callback to execute when the Promise is settled (fulfilled or rejected).
     * @returns A Promise for the completion of the callback.
     */
    finally(onfinally?: (() => void) | undefined | null): $Utils.JsPromise<T>
  }




  /**
   * Fields of the FunalyticsScore model
   */
  interface FunalyticsScoreFieldRefs {
    readonly id: FieldRef<"FunalyticsScore", 'String'>
    readonly eventId: FieldRef<"FunalyticsScore", 'Int'>
    readonly communityVibe: FieldRef<"FunalyticsScore", 'Int'>
    readonly familyFun: FieldRef<"FunalyticsScore", 'Int'>
    readonly overallScore: FieldRef<"FunalyticsScore", 'Int'>
    readonly reasoning: FieldRef<"FunalyticsScore", 'String'>
    readonly computedAt: FieldRef<"FunalyticsScore", 'DateTime'>
  }
    

  // Custom InputTypes
  /**
   * FunalyticsScore findUnique
   */
  export type FunalyticsScoreFindUniqueArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the FunalyticsScore
     */
    select?: FunalyticsScoreSelect<ExtArgs> | null
    /**
     * Omit specific fields from the FunalyticsScore
     */
    omit?: FunalyticsScoreOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: FunalyticsScoreInclude<ExtArgs> | null
    /**
     * Filter, which FunalyticsScore to fetch.
     */
    where: FunalyticsScoreWhereUniqueInput
  }

  /**
   * FunalyticsScore findUniqueOrThrow
   */
  export type FunalyticsScoreFindUniqueOrThrowArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the FunalyticsScore
     */
    select?: FunalyticsScoreSelect<ExtArgs> | null
    /**
     * Omit specific fields from the FunalyticsScore
     */
    omit?: FunalyticsScoreOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: FunalyticsScoreInclude<ExtArgs> | null
    /**
     * Filter, which FunalyticsScore to fetch.
     */
    where: FunalyticsScoreWhereUniqueInput
  }

  /**
   * FunalyticsScore findFirst
   */
  export type FunalyticsScoreFindFirstArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the FunalyticsScore
     */
    select?: FunalyticsScoreSelect<ExtArgs> | null
    /**
     * Omit specific fields from the FunalyticsScore
     */
    omit?: FunalyticsScoreOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: FunalyticsScoreInclude<ExtArgs> | null
    /**
     * Filter, which FunalyticsScore to fetch.
     */
    where?: FunalyticsScoreWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of FunalyticsScores to fetch.
     */
    orderBy?: FunalyticsScoreOrderByWithRelationInput | FunalyticsScoreOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for FunalyticsScores.
     */
    cursor?: FunalyticsScoreWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` FunalyticsScores from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` FunalyticsScores.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of FunalyticsScores.
     */
    distinct?: FunalyticsScoreScalarFieldEnum | FunalyticsScoreScalarFieldEnum[]
  }

  /**
   * FunalyticsScore findFirstOrThrow
   */
  export type FunalyticsScoreFindFirstOrThrowArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the FunalyticsScore
     */
    select?: FunalyticsScoreSelect<ExtArgs> | null
    /**
     * Omit specific fields from the FunalyticsScore
     */
    omit?: FunalyticsScoreOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: FunalyticsScoreInclude<ExtArgs> | null
    /**
     * Filter, which FunalyticsScore to fetch.
     */
    where?: FunalyticsScoreWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of FunalyticsScores to fetch.
     */
    orderBy?: FunalyticsScoreOrderByWithRelationInput | FunalyticsScoreOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for searching for FunalyticsScores.
     */
    cursor?: FunalyticsScoreWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` FunalyticsScores from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` FunalyticsScores.
     */
    skip?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/distinct Distinct Docs}
     * 
     * Filter by unique combinations of FunalyticsScores.
     */
    distinct?: FunalyticsScoreScalarFieldEnum | FunalyticsScoreScalarFieldEnum[]
  }

  /**
   * FunalyticsScore findMany
   */
  export type FunalyticsScoreFindManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the FunalyticsScore
     */
    select?: FunalyticsScoreSelect<ExtArgs> | null
    /**
     * Omit specific fields from the FunalyticsScore
     */
    omit?: FunalyticsScoreOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: FunalyticsScoreInclude<ExtArgs> | null
    /**
     * Filter, which FunalyticsScores to fetch.
     */
    where?: FunalyticsScoreWhereInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/sorting Sorting Docs}
     * 
     * Determine the order of FunalyticsScores to fetch.
     */
    orderBy?: FunalyticsScoreOrderByWithRelationInput | FunalyticsScoreOrderByWithRelationInput[]
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination#cursor-based-pagination Cursor Docs}
     * 
     * Sets the position for listing FunalyticsScores.
     */
    cursor?: FunalyticsScoreWhereUniqueInput
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Take `±n` FunalyticsScores from the position of the cursor.
     */
    take?: number
    /**
     * {@link https://www.prisma.io/docs/concepts/components/prisma-client/pagination Pagination Docs}
     * 
     * Skip the first `n` FunalyticsScores.
     */
    skip?: number
    distinct?: FunalyticsScoreScalarFieldEnum | FunalyticsScoreScalarFieldEnum[]
  }

  /**
   * FunalyticsScore create
   */
  export type FunalyticsScoreCreateArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the FunalyticsScore
     */
    select?: FunalyticsScoreSelect<ExtArgs> | null
    /**
     * Omit specific fields from the FunalyticsScore
     */
    omit?: FunalyticsScoreOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: FunalyticsScoreInclude<ExtArgs> | null
    /**
     * The data needed to create a FunalyticsScore.
     */
    data: XOR<FunalyticsScoreCreateInput, FunalyticsScoreUncheckedCreateInput>
  }

  /**
   * FunalyticsScore createMany
   */
  export type FunalyticsScoreCreateManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * The data used to create many FunalyticsScores.
     */
    data: FunalyticsScoreCreateManyInput | FunalyticsScoreCreateManyInput[]
    skipDuplicates?: boolean
  }

  /**
   * FunalyticsScore createManyAndReturn
   */
  export type FunalyticsScoreCreateManyAndReturnArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the FunalyticsScore
     */
    select?: FunalyticsScoreSelectCreateManyAndReturn<ExtArgs> | null
    /**
     * Omit specific fields from the FunalyticsScore
     */
    omit?: FunalyticsScoreOmit<ExtArgs> | null
    /**
     * The data used to create many FunalyticsScores.
     */
    data: FunalyticsScoreCreateManyInput | FunalyticsScoreCreateManyInput[]
    skipDuplicates?: boolean
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: FunalyticsScoreIncludeCreateManyAndReturn<ExtArgs> | null
  }

  /**
   * FunalyticsScore update
   */
  export type FunalyticsScoreUpdateArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the FunalyticsScore
     */
    select?: FunalyticsScoreSelect<ExtArgs> | null
    /**
     * Omit specific fields from the FunalyticsScore
     */
    omit?: FunalyticsScoreOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: FunalyticsScoreInclude<ExtArgs> | null
    /**
     * The data needed to update a FunalyticsScore.
     */
    data: XOR<FunalyticsScoreUpdateInput, FunalyticsScoreUncheckedUpdateInput>
    /**
     * Choose, which FunalyticsScore to update.
     */
    where: FunalyticsScoreWhereUniqueInput
  }

  /**
   * FunalyticsScore updateMany
   */
  export type FunalyticsScoreUpdateManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * The data used to update FunalyticsScores.
     */
    data: XOR<FunalyticsScoreUpdateManyMutationInput, FunalyticsScoreUncheckedUpdateManyInput>
    /**
     * Filter which FunalyticsScores to update
     */
    where?: FunalyticsScoreWhereInput
    /**
     * Limit how many FunalyticsScores to update.
     */
    limit?: number
  }

  /**
   * FunalyticsScore updateManyAndReturn
   */
  export type FunalyticsScoreUpdateManyAndReturnArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the FunalyticsScore
     */
    select?: FunalyticsScoreSelectUpdateManyAndReturn<ExtArgs> | null
    /**
     * Omit specific fields from the FunalyticsScore
     */
    omit?: FunalyticsScoreOmit<ExtArgs> | null
    /**
     * The data used to update FunalyticsScores.
     */
    data: XOR<FunalyticsScoreUpdateManyMutationInput, FunalyticsScoreUncheckedUpdateManyInput>
    /**
     * Filter which FunalyticsScores to update
     */
    where?: FunalyticsScoreWhereInput
    /**
     * Limit how many FunalyticsScores to update.
     */
    limit?: number
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: FunalyticsScoreIncludeUpdateManyAndReturn<ExtArgs> | null
  }

  /**
   * FunalyticsScore upsert
   */
  export type FunalyticsScoreUpsertArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the FunalyticsScore
     */
    select?: FunalyticsScoreSelect<ExtArgs> | null
    /**
     * Omit specific fields from the FunalyticsScore
     */
    omit?: FunalyticsScoreOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: FunalyticsScoreInclude<ExtArgs> | null
    /**
     * The filter to search for the FunalyticsScore to update in case it exists.
     */
    where: FunalyticsScoreWhereUniqueInput
    /**
     * In case the FunalyticsScore found by the `where` argument doesn't exist, create a new FunalyticsScore with this data.
     */
    create: XOR<FunalyticsScoreCreateInput, FunalyticsScoreUncheckedCreateInput>
    /**
     * In case the FunalyticsScore was found with the provided `where` argument, update it with this data.
     */
    update: XOR<FunalyticsScoreUpdateInput, FunalyticsScoreUncheckedUpdateInput>
  }

  /**
   * FunalyticsScore delete
   */
  export type FunalyticsScoreDeleteArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the FunalyticsScore
     */
    select?: FunalyticsScoreSelect<ExtArgs> | null
    /**
     * Omit specific fields from the FunalyticsScore
     */
    omit?: FunalyticsScoreOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: FunalyticsScoreInclude<ExtArgs> | null
    /**
     * Filter which FunalyticsScore to delete.
     */
    where: FunalyticsScoreWhereUniqueInput
  }

  /**
   * FunalyticsScore deleteMany
   */
  export type FunalyticsScoreDeleteManyArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Filter which FunalyticsScores to delete
     */
    where?: FunalyticsScoreWhereInput
    /**
     * Limit how many FunalyticsScores to delete.
     */
    limit?: number
  }

  /**
   * FunalyticsScore without action
   */
  export type FunalyticsScoreDefaultArgs<ExtArgs extends $Extensions.InternalArgs = $Extensions.DefaultArgs> = {
    /**
     * Select specific fields to fetch from the FunalyticsScore
     */
    select?: FunalyticsScoreSelect<ExtArgs> | null
    /**
     * Omit specific fields from the FunalyticsScore
     */
    omit?: FunalyticsScoreOmit<ExtArgs> | null
    /**
     * Choose, which related nodes to fetch as well
     */
    include?: FunalyticsScoreInclude<ExtArgs> | null
  }


  /**
   * Enums
   */

  export const TransactionIsolationLevel: {
    ReadUncommitted: 'ReadUncommitted',
    ReadCommitted: 'ReadCommitted',
    RepeatableRead: 'RepeatableRead',
    Serializable: 'Serializable'
  };

  export type TransactionIsolationLevel = (typeof TransactionIsolationLevel)[keyof typeof TransactionIsolationLevel]


  export const EventScalarFieldEnum: {
    id: 'id',
    title: 'title',
    description: 'description',
    startTime: 'startTime',
    endTime: 'endTime',
    location: 'location',
    city: 'city',
    state: 'state',
    zipCode: 'zipCode',
    latitude: 'latitude',
    longitude: 'longitude',
    category: 'category',
    organizerId: 'organizerId',
    venueId: 'venueId',
    status: 'status',
    created_at: 'created_at',
    updated_at: 'updated_at'
  };

  export type EventScalarFieldEnum = (typeof EventScalarFieldEnum)[keyof typeof EventScalarFieldEnum]


  export const UserScalarFieldEnum: {
    id: 'id',
    first_name: 'first_name',
    last_name: 'last_name',
    company_name: 'company_name',
    email: 'email',
    password_hash: 'password_hash',
    phone: 'phone',
    is_organizer: 'is_organizer',
    is_sponsor: 'is_sponsor',
    is_vendor: 'is_vendor',
    is_admin: 'is_admin',
    is_active: 'is_active',
    created_at: 'created_at',
    updated_at: 'updated_at'
  };

  export type UserScalarFieldEnum = (typeof UserScalarFieldEnum)[keyof typeof UserScalarFieldEnum]


  export const VenueScalarFieldEnum: {
    id: 'id',
    name: 'name',
    address: 'address',
    city: 'city',
    state: 'state',
    zip_code: 'zip_code',
    latitude: 'latitude',
    longitude: 'longitude',
    capacity: 'capacity',
    venue_type_id: 'venue_type_id',
    created_at: 'created_at',
    updated_at: 'updated_at'
  };

  export type VenueScalarFieldEnum = (typeof VenueScalarFieldEnum)[keyof typeof VenueScalarFieldEnum]


  export const FunalyticsScoreScalarFieldEnum: {
    id: 'id',
    eventId: 'eventId',
    communityVibe: 'communityVibe',
    familyFun: 'familyFun',
    overallScore: 'overallScore',
    reasoning: 'reasoning',
    computedAt: 'computedAt'
  };

  export type FunalyticsScoreScalarFieldEnum = (typeof FunalyticsScoreScalarFieldEnum)[keyof typeof FunalyticsScoreScalarFieldEnum]


  export const SortOrder: {
    asc: 'asc',
    desc: 'desc'
  };

  export type SortOrder = (typeof SortOrder)[keyof typeof SortOrder]


  export const QueryMode: {
    default: 'default',
    insensitive: 'insensitive'
  };

  export type QueryMode = (typeof QueryMode)[keyof typeof QueryMode]


  export const NullsOrder: {
    first: 'first',
    last: 'last'
  };

  export type NullsOrder = (typeof NullsOrder)[keyof typeof NullsOrder]


  /**
   * Field references
   */


  /**
   * Reference to a field of type 'Int'
   */
  export type IntFieldRefInput<$PrismaModel> = FieldRefInputType<$PrismaModel, 'Int'>
    


  /**
   * Reference to a field of type 'Int[]'
   */
  export type ListIntFieldRefInput<$PrismaModel> = FieldRefInputType<$PrismaModel, 'Int[]'>
    


  /**
   * Reference to a field of type 'String'
   */
  export type StringFieldRefInput<$PrismaModel> = FieldRefInputType<$PrismaModel, 'String'>
    


  /**
   * Reference to a field of type 'String[]'
   */
  export type ListStringFieldRefInput<$PrismaModel> = FieldRefInputType<$PrismaModel, 'String[]'>
    


  /**
   * Reference to a field of type 'DateTime'
   */
  export type DateTimeFieldRefInput<$PrismaModel> = FieldRefInputType<$PrismaModel, 'DateTime'>
    


  /**
   * Reference to a field of type 'DateTime[]'
   */
  export type ListDateTimeFieldRefInput<$PrismaModel> = FieldRefInputType<$PrismaModel, 'DateTime[]'>
    


  /**
   * Reference to a field of type 'Float'
   */
  export type FloatFieldRefInput<$PrismaModel> = FieldRefInputType<$PrismaModel, 'Float'>
    


  /**
   * Reference to a field of type 'Float[]'
   */
  export type ListFloatFieldRefInput<$PrismaModel> = FieldRefInputType<$PrismaModel, 'Float[]'>
    


  /**
   * Reference to a field of type 'Boolean'
   */
  export type BooleanFieldRefInput<$PrismaModel> = FieldRefInputType<$PrismaModel, 'Boolean'>
    
  /**
   * Deep Input Types
   */


  export type EventWhereInput = {
    AND?: EventWhereInput | EventWhereInput[]
    OR?: EventWhereInput[]
    NOT?: EventWhereInput | EventWhereInput[]
    id?: IntFilter<"Event"> | number
    title?: StringFilter<"Event"> | string
    description?: StringNullableFilter<"Event"> | string | null
    startTime?: DateTimeFilter<"Event"> | Date | string
    endTime?: DateTimeNullableFilter<"Event"> | Date | string | null
    location?: StringNullableFilter<"Event"> | string | null
    city?: StringNullableFilter<"Event"> | string | null
    state?: StringNullableFilter<"Event"> | string | null
    zipCode?: StringNullableFilter<"Event"> | string | null
    latitude?: FloatNullableFilter<"Event"> | number | null
    longitude?: FloatNullableFilter<"Event"> | number | null
    category?: StringNullableFilter<"Event"> | string | null
    organizerId?: IntNullableFilter<"Event"> | number | null
    venueId?: IntNullableFilter<"Event"> | number | null
    status?: StringNullableFilter<"Event"> | string | null
    created_at?: DateTimeNullableFilter<"Event"> | Date | string | null
    updated_at?: DateTimeNullableFilter<"Event"> | Date | string | null
    organizer?: XOR<UserNullableScalarRelationFilter, UserWhereInput> | null
    venue?: XOR<VenueNullableScalarRelationFilter, VenueWhereInput> | null
    funalytics?: FunalyticsScoreListRelationFilter
  }

  export type EventOrderByWithRelationInput = {
    id?: SortOrder
    title?: SortOrder
    description?: SortOrderInput | SortOrder
    startTime?: SortOrder
    endTime?: SortOrderInput | SortOrder
    location?: SortOrderInput | SortOrder
    city?: SortOrderInput | SortOrder
    state?: SortOrderInput | SortOrder
    zipCode?: SortOrderInput | SortOrder
    latitude?: SortOrderInput | SortOrder
    longitude?: SortOrderInput | SortOrder
    category?: SortOrderInput | SortOrder
    organizerId?: SortOrderInput | SortOrder
    venueId?: SortOrderInput | SortOrder
    status?: SortOrderInput | SortOrder
    created_at?: SortOrderInput | SortOrder
    updated_at?: SortOrderInput | SortOrder
    organizer?: UserOrderByWithRelationInput
    venue?: VenueOrderByWithRelationInput
    funalytics?: FunalyticsScoreOrderByRelationAggregateInput
  }

  export type EventWhereUniqueInput = Prisma.AtLeast<{
    id?: number
    AND?: EventWhereInput | EventWhereInput[]
    OR?: EventWhereInput[]
    NOT?: EventWhereInput | EventWhereInput[]
    title?: StringFilter<"Event"> | string
    description?: StringNullableFilter<"Event"> | string | null
    startTime?: DateTimeFilter<"Event"> | Date | string
    endTime?: DateTimeNullableFilter<"Event"> | Date | string | null
    location?: StringNullableFilter<"Event"> | string | null
    city?: StringNullableFilter<"Event"> | string | null
    state?: StringNullableFilter<"Event"> | string | null
    zipCode?: StringNullableFilter<"Event"> | string | null
    latitude?: FloatNullableFilter<"Event"> | number | null
    longitude?: FloatNullableFilter<"Event"> | number | null
    category?: StringNullableFilter<"Event"> | string | null
    organizerId?: IntNullableFilter<"Event"> | number | null
    venueId?: IntNullableFilter<"Event"> | number | null
    status?: StringNullableFilter<"Event"> | string | null
    created_at?: DateTimeNullableFilter<"Event"> | Date | string | null
    updated_at?: DateTimeNullableFilter<"Event"> | Date | string | null
    organizer?: XOR<UserNullableScalarRelationFilter, UserWhereInput> | null
    venue?: XOR<VenueNullableScalarRelationFilter, VenueWhereInput> | null
    funalytics?: FunalyticsScoreListRelationFilter
  }, "id">

  export type EventOrderByWithAggregationInput = {
    id?: SortOrder
    title?: SortOrder
    description?: SortOrderInput | SortOrder
    startTime?: SortOrder
    endTime?: SortOrderInput | SortOrder
    location?: SortOrderInput | SortOrder
    city?: SortOrderInput | SortOrder
    state?: SortOrderInput | SortOrder
    zipCode?: SortOrderInput | SortOrder
    latitude?: SortOrderInput | SortOrder
    longitude?: SortOrderInput | SortOrder
    category?: SortOrderInput | SortOrder
    organizerId?: SortOrderInput | SortOrder
    venueId?: SortOrderInput | SortOrder
    status?: SortOrderInput | SortOrder
    created_at?: SortOrderInput | SortOrder
    updated_at?: SortOrderInput | SortOrder
    _count?: EventCountOrderByAggregateInput
    _avg?: EventAvgOrderByAggregateInput
    _max?: EventMaxOrderByAggregateInput
    _min?: EventMinOrderByAggregateInput
    _sum?: EventSumOrderByAggregateInput
  }

  export type EventScalarWhereWithAggregatesInput = {
    AND?: EventScalarWhereWithAggregatesInput | EventScalarWhereWithAggregatesInput[]
    OR?: EventScalarWhereWithAggregatesInput[]
    NOT?: EventScalarWhereWithAggregatesInput | EventScalarWhereWithAggregatesInput[]
    id?: IntWithAggregatesFilter<"Event"> | number
    title?: StringWithAggregatesFilter<"Event"> | string
    description?: StringNullableWithAggregatesFilter<"Event"> | string | null
    startTime?: DateTimeWithAggregatesFilter<"Event"> | Date | string
    endTime?: DateTimeNullableWithAggregatesFilter<"Event"> | Date | string | null
    location?: StringNullableWithAggregatesFilter<"Event"> | string | null
    city?: StringNullableWithAggregatesFilter<"Event"> | string | null
    state?: StringNullableWithAggregatesFilter<"Event"> | string | null
    zipCode?: StringNullableWithAggregatesFilter<"Event"> | string | null
    latitude?: FloatNullableWithAggregatesFilter<"Event"> | number | null
    longitude?: FloatNullableWithAggregatesFilter<"Event"> | number | null
    category?: StringNullableWithAggregatesFilter<"Event"> | string | null
    organizerId?: IntNullableWithAggregatesFilter<"Event"> | number | null
    venueId?: IntNullableWithAggregatesFilter<"Event"> | number | null
    status?: StringNullableWithAggregatesFilter<"Event"> | string | null
    created_at?: DateTimeNullableWithAggregatesFilter<"Event"> | Date | string | null
    updated_at?: DateTimeNullableWithAggregatesFilter<"Event"> | Date | string | null
  }

  export type UserWhereInput = {
    AND?: UserWhereInput | UserWhereInput[]
    OR?: UserWhereInput[]
    NOT?: UserWhereInput | UserWhereInput[]
    id?: IntFilter<"User"> | number
    first_name?: StringNullableFilter<"User"> | string | null
    last_name?: StringNullableFilter<"User"> | string | null
    company_name?: StringNullableFilter<"User"> | string | null
    email?: StringFilter<"User"> | string
    password_hash?: StringNullableFilter<"User"> | string | null
    phone?: StringNullableFilter<"User"> | string | null
    is_organizer?: BoolNullableFilter<"User"> | boolean | null
    is_sponsor?: BoolNullableFilter<"User"> | boolean | null
    is_vendor?: BoolNullableFilter<"User"> | boolean | null
    is_admin?: BoolNullableFilter<"User"> | boolean | null
    is_active?: BoolNullableFilter<"User"> | boolean | null
    created_at?: DateTimeNullableFilter<"User"> | Date | string | null
    updated_at?: DateTimeNullableFilter<"User"> | Date | string | null
    events?: EventListRelationFilter
  }

  export type UserOrderByWithRelationInput = {
    id?: SortOrder
    first_name?: SortOrderInput | SortOrder
    last_name?: SortOrderInput | SortOrder
    company_name?: SortOrderInput | SortOrder
    email?: SortOrder
    password_hash?: SortOrderInput | SortOrder
    phone?: SortOrderInput | SortOrder
    is_organizer?: SortOrderInput | SortOrder
    is_sponsor?: SortOrderInput | SortOrder
    is_vendor?: SortOrderInput | SortOrder
    is_admin?: SortOrderInput | SortOrder
    is_active?: SortOrderInput | SortOrder
    created_at?: SortOrderInput | SortOrder
    updated_at?: SortOrderInput | SortOrder
    events?: EventOrderByRelationAggregateInput
  }

  export type UserWhereUniqueInput = Prisma.AtLeast<{
    id?: number
    email?: string
    AND?: UserWhereInput | UserWhereInput[]
    OR?: UserWhereInput[]
    NOT?: UserWhereInput | UserWhereInput[]
    first_name?: StringNullableFilter<"User"> | string | null
    last_name?: StringNullableFilter<"User"> | string | null
    company_name?: StringNullableFilter<"User"> | string | null
    password_hash?: StringNullableFilter<"User"> | string | null
    phone?: StringNullableFilter<"User"> | string | null
    is_organizer?: BoolNullableFilter<"User"> | boolean | null
    is_sponsor?: BoolNullableFilter<"User"> | boolean | null
    is_vendor?: BoolNullableFilter<"User"> | boolean | null
    is_admin?: BoolNullableFilter<"User"> | boolean | null
    is_active?: BoolNullableFilter<"User"> | boolean | null
    created_at?: DateTimeNullableFilter<"User"> | Date | string | null
    updated_at?: DateTimeNullableFilter<"User"> | Date | string | null
    events?: EventListRelationFilter
  }, "id" | "email">

  export type UserOrderByWithAggregationInput = {
    id?: SortOrder
    first_name?: SortOrderInput | SortOrder
    last_name?: SortOrderInput | SortOrder
    company_name?: SortOrderInput | SortOrder
    email?: SortOrder
    password_hash?: SortOrderInput | SortOrder
    phone?: SortOrderInput | SortOrder
    is_organizer?: SortOrderInput | SortOrder
    is_sponsor?: SortOrderInput | SortOrder
    is_vendor?: SortOrderInput | SortOrder
    is_admin?: SortOrderInput | SortOrder
    is_active?: SortOrderInput | SortOrder
    created_at?: SortOrderInput | SortOrder
    updated_at?: SortOrderInput | SortOrder
    _count?: UserCountOrderByAggregateInput
    _avg?: UserAvgOrderByAggregateInput
    _max?: UserMaxOrderByAggregateInput
    _min?: UserMinOrderByAggregateInput
    _sum?: UserSumOrderByAggregateInput
  }

  export type UserScalarWhereWithAggregatesInput = {
    AND?: UserScalarWhereWithAggregatesInput | UserScalarWhereWithAggregatesInput[]
    OR?: UserScalarWhereWithAggregatesInput[]
    NOT?: UserScalarWhereWithAggregatesInput | UserScalarWhereWithAggregatesInput[]
    id?: IntWithAggregatesFilter<"User"> | number
    first_name?: StringNullableWithAggregatesFilter<"User"> | string | null
    last_name?: StringNullableWithAggregatesFilter<"User"> | string | null
    company_name?: StringNullableWithAggregatesFilter<"User"> | string | null
    email?: StringWithAggregatesFilter<"User"> | string
    password_hash?: StringNullableWithAggregatesFilter<"User"> | string | null
    phone?: StringNullableWithAggregatesFilter<"User"> | string | null
    is_organizer?: BoolNullableWithAggregatesFilter<"User"> | boolean | null
    is_sponsor?: BoolNullableWithAggregatesFilter<"User"> | boolean | null
    is_vendor?: BoolNullableWithAggregatesFilter<"User"> | boolean | null
    is_admin?: BoolNullableWithAggregatesFilter<"User"> | boolean | null
    is_active?: BoolNullableWithAggregatesFilter<"User"> | boolean | null
    created_at?: DateTimeNullableWithAggregatesFilter<"User"> | Date | string | null
    updated_at?: DateTimeNullableWithAggregatesFilter<"User"> | Date | string | null
  }

  export type VenueWhereInput = {
    AND?: VenueWhereInput | VenueWhereInput[]
    OR?: VenueWhereInput[]
    NOT?: VenueWhereInput | VenueWhereInput[]
    id?: IntFilter<"Venue"> | number
    name?: StringNullableFilter<"Venue"> | string | null
    address?: StringNullableFilter<"Venue"> | string | null
    city?: StringNullableFilter<"Venue"> | string | null
    state?: StringNullableFilter<"Venue"> | string | null
    zip_code?: StringNullableFilter<"Venue"> | string | null
    latitude?: FloatNullableFilter<"Venue"> | number | null
    longitude?: FloatNullableFilter<"Venue"> | number | null
    capacity?: IntNullableFilter<"Venue"> | number | null
    venue_type_id?: IntNullableFilter<"Venue"> | number | null
    created_at?: DateTimeNullableFilter<"Venue"> | Date | string | null
    updated_at?: DateTimeNullableFilter<"Venue"> | Date | string | null
    events?: EventListRelationFilter
  }

  export type VenueOrderByWithRelationInput = {
    id?: SortOrder
    name?: SortOrderInput | SortOrder
    address?: SortOrderInput | SortOrder
    city?: SortOrderInput | SortOrder
    state?: SortOrderInput | SortOrder
    zip_code?: SortOrderInput | SortOrder
    latitude?: SortOrderInput | SortOrder
    longitude?: SortOrderInput | SortOrder
    capacity?: SortOrderInput | SortOrder
    venue_type_id?: SortOrderInput | SortOrder
    created_at?: SortOrderInput | SortOrder
    updated_at?: SortOrderInput | SortOrder
    events?: EventOrderByRelationAggregateInput
  }

  export type VenueWhereUniqueInput = Prisma.AtLeast<{
    id?: number
    AND?: VenueWhereInput | VenueWhereInput[]
    OR?: VenueWhereInput[]
    NOT?: VenueWhereInput | VenueWhereInput[]
    name?: StringNullableFilter<"Venue"> | string | null
    address?: StringNullableFilter<"Venue"> | string | null
    city?: StringNullableFilter<"Venue"> | string | null
    state?: StringNullableFilter<"Venue"> | string | null
    zip_code?: StringNullableFilter<"Venue"> | string | null
    latitude?: FloatNullableFilter<"Venue"> | number | null
    longitude?: FloatNullableFilter<"Venue"> | number | null
    capacity?: IntNullableFilter<"Venue"> | number | null
    venue_type_id?: IntNullableFilter<"Venue"> | number | null
    created_at?: DateTimeNullableFilter<"Venue"> | Date | string | null
    updated_at?: DateTimeNullableFilter<"Venue"> | Date | string | null
    events?: EventListRelationFilter
  }, "id">

  export type VenueOrderByWithAggregationInput = {
    id?: SortOrder
    name?: SortOrderInput | SortOrder
    address?: SortOrderInput | SortOrder
    city?: SortOrderInput | SortOrder
    state?: SortOrderInput | SortOrder
    zip_code?: SortOrderInput | SortOrder
    latitude?: SortOrderInput | SortOrder
    longitude?: SortOrderInput | SortOrder
    capacity?: SortOrderInput | SortOrder
    venue_type_id?: SortOrderInput | SortOrder
    created_at?: SortOrderInput | SortOrder
    updated_at?: SortOrderInput | SortOrder
    _count?: VenueCountOrderByAggregateInput
    _avg?: VenueAvgOrderByAggregateInput
    _max?: VenueMaxOrderByAggregateInput
    _min?: VenueMinOrderByAggregateInput
    _sum?: VenueSumOrderByAggregateInput
  }

  export type VenueScalarWhereWithAggregatesInput = {
    AND?: VenueScalarWhereWithAggregatesInput | VenueScalarWhereWithAggregatesInput[]
    OR?: VenueScalarWhereWithAggregatesInput[]
    NOT?: VenueScalarWhereWithAggregatesInput | VenueScalarWhereWithAggregatesInput[]
    id?: IntWithAggregatesFilter<"Venue"> | number
    name?: StringNullableWithAggregatesFilter<"Venue"> | string | null
    address?: StringNullableWithAggregatesFilter<"Venue"> | string | null
    city?: StringNullableWithAggregatesFilter<"Venue"> | string | null
    state?: StringNullableWithAggregatesFilter<"Venue"> | string | null
    zip_code?: StringNullableWithAggregatesFilter<"Venue"> | string | null
    latitude?: FloatNullableWithAggregatesFilter<"Venue"> | number | null
    longitude?: FloatNullableWithAggregatesFilter<"Venue"> | number | null
    capacity?: IntNullableWithAggregatesFilter<"Venue"> | number | null
    venue_type_id?: IntNullableWithAggregatesFilter<"Venue"> | number | null
    created_at?: DateTimeNullableWithAggregatesFilter<"Venue"> | Date | string | null
    updated_at?: DateTimeNullableWithAggregatesFilter<"Venue"> | Date | string | null
  }

  export type FunalyticsScoreWhereInput = {
    AND?: FunalyticsScoreWhereInput | FunalyticsScoreWhereInput[]
    OR?: FunalyticsScoreWhereInput[]
    NOT?: FunalyticsScoreWhereInput | FunalyticsScoreWhereInput[]
    id?: StringFilter<"FunalyticsScore"> | string
    eventId?: IntFilter<"FunalyticsScore"> | number
    communityVibe?: IntNullableFilter<"FunalyticsScore"> | number | null
    familyFun?: IntNullableFilter<"FunalyticsScore"> | number | null
    overallScore?: IntNullableFilter<"FunalyticsScore"> | number | null
    reasoning?: StringNullableFilter<"FunalyticsScore"> | string | null
    computedAt?: DateTimeFilter<"FunalyticsScore"> | Date | string
    event?: XOR<EventScalarRelationFilter, EventWhereInput>
  }

  export type FunalyticsScoreOrderByWithRelationInput = {
    id?: SortOrder
    eventId?: SortOrder
    communityVibe?: SortOrderInput | SortOrder
    familyFun?: SortOrderInput | SortOrder
    overallScore?: SortOrderInput | SortOrder
    reasoning?: SortOrderInput | SortOrder
    computedAt?: SortOrder
    event?: EventOrderByWithRelationInput
  }

  export type FunalyticsScoreWhereUniqueInput = Prisma.AtLeast<{
    id?: string
    AND?: FunalyticsScoreWhereInput | FunalyticsScoreWhereInput[]
    OR?: FunalyticsScoreWhereInput[]
    NOT?: FunalyticsScoreWhereInput | FunalyticsScoreWhereInput[]
    eventId?: IntFilter<"FunalyticsScore"> | number
    communityVibe?: IntNullableFilter<"FunalyticsScore"> | number | null
    familyFun?: IntNullableFilter<"FunalyticsScore"> | number | null
    overallScore?: IntNullableFilter<"FunalyticsScore"> | number | null
    reasoning?: StringNullableFilter<"FunalyticsScore"> | string | null
    computedAt?: DateTimeFilter<"FunalyticsScore"> | Date | string
    event?: XOR<EventScalarRelationFilter, EventWhereInput>
  }, "id">

  export type FunalyticsScoreOrderByWithAggregationInput = {
    id?: SortOrder
    eventId?: SortOrder
    communityVibe?: SortOrderInput | SortOrder
    familyFun?: SortOrderInput | SortOrder
    overallScore?: SortOrderInput | SortOrder
    reasoning?: SortOrderInput | SortOrder
    computedAt?: SortOrder
    _count?: FunalyticsScoreCountOrderByAggregateInput
    _avg?: FunalyticsScoreAvgOrderByAggregateInput
    _max?: FunalyticsScoreMaxOrderByAggregateInput
    _min?: FunalyticsScoreMinOrderByAggregateInput
    _sum?: FunalyticsScoreSumOrderByAggregateInput
  }

  export type FunalyticsScoreScalarWhereWithAggregatesInput = {
    AND?: FunalyticsScoreScalarWhereWithAggregatesInput | FunalyticsScoreScalarWhereWithAggregatesInput[]
    OR?: FunalyticsScoreScalarWhereWithAggregatesInput[]
    NOT?: FunalyticsScoreScalarWhereWithAggregatesInput | FunalyticsScoreScalarWhereWithAggregatesInput[]
    id?: StringWithAggregatesFilter<"FunalyticsScore"> | string
    eventId?: IntWithAggregatesFilter<"FunalyticsScore"> | number
    communityVibe?: IntNullableWithAggregatesFilter<"FunalyticsScore"> | number | null
    familyFun?: IntNullableWithAggregatesFilter<"FunalyticsScore"> | number | null
    overallScore?: IntNullableWithAggregatesFilter<"FunalyticsScore"> | number | null
    reasoning?: StringNullableWithAggregatesFilter<"FunalyticsScore"> | string | null
    computedAt?: DateTimeWithAggregatesFilter<"FunalyticsScore"> | Date | string
  }

  export type EventCreateInput = {
    title: string
    description?: string | null
    startTime: Date | string
    endTime?: Date | string | null
    location?: string | null
    city?: string | null
    state?: string | null
    zipCode?: string | null
    latitude?: number | null
    longitude?: number | null
    category?: string | null
    status?: string | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
    organizer?: UserCreateNestedOneWithoutEventsInput
    venue?: VenueCreateNestedOneWithoutEventsInput
    funalytics?: FunalyticsScoreCreateNestedManyWithoutEventInput
  }

  export type EventUncheckedCreateInput = {
    id?: number
    title: string
    description?: string | null
    startTime: Date | string
    endTime?: Date | string | null
    location?: string | null
    city?: string | null
    state?: string | null
    zipCode?: string | null
    latitude?: number | null
    longitude?: number | null
    category?: string | null
    organizerId?: number | null
    venueId?: number | null
    status?: string | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
    funalytics?: FunalyticsScoreUncheckedCreateNestedManyWithoutEventInput
  }

  export type EventUpdateInput = {
    title?: StringFieldUpdateOperationsInput | string
    description?: NullableStringFieldUpdateOperationsInput | string | null
    startTime?: DateTimeFieldUpdateOperationsInput | Date | string
    endTime?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    location?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zipCode?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    category?: NullableStringFieldUpdateOperationsInput | string | null
    status?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    organizer?: UserUpdateOneWithoutEventsNestedInput
    venue?: VenueUpdateOneWithoutEventsNestedInput
    funalytics?: FunalyticsScoreUpdateManyWithoutEventNestedInput
  }

  export type EventUncheckedUpdateInput = {
    id?: IntFieldUpdateOperationsInput | number
    title?: StringFieldUpdateOperationsInput | string
    description?: NullableStringFieldUpdateOperationsInput | string | null
    startTime?: DateTimeFieldUpdateOperationsInput | Date | string
    endTime?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    location?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zipCode?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    category?: NullableStringFieldUpdateOperationsInput | string | null
    organizerId?: NullableIntFieldUpdateOperationsInput | number | null
    venueId?: NullableIntFieldUpdateOperationsInput | number | null
    status?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    funalytics?: FunalyticsScoreUncheckedUpdateManyWithoutEventNestedInput
  }

  export type EventCreateManyInput = {
    id?: number
    title: string
    description?: string | null
    startTime: Date | string
    endTime?: Date | string | null
    location?: string | null
    city?: string | null
    state?: string | null
    zipCode?: string | null
    latitude?: number | null
    longitude?: number | null
    category?: string | null
    organizerId?: number | null
    venueId?: number | null
    status?: string | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
  }

  export type EventUpdateManyMutationInput = {
    title?: StringFieldUpdateOperationsInput | string
    description?: NullableStringFieldUpdateOperationsInput | string | null
    startTime?: DateTimeFieldUpdateOperationsInput | Date | string
    endTime?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    location?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zipCode?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    category?: NullableStringFieldUpdateOperationsInput | string | null
    status?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
  }

  export type EventUncheckedUpdateManyInput = {
    id?: IntFieldUpdateOperationsInput | number
    title?: StringFieldUpdateOperationsInput | string
    description?: NullableStringFieldUpdateOperationsInput | string | null
    startTime?: DateTimeFieldUpdateOperationsInput | Date | string
    endTime?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    location?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zipCode?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    category?: NullableStringFieldUpdateOperationsInput | string | null
    organizerId?: NullableIntFieldUpdateOperationsInput | number | null
    venueId?: NullableIntFieldUpdateOperationsInput | number | null
    status?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
  }

  export type UserCreateInput = {
    first_name?: string | null
    last_name?: string | null
    company_name?: string | null
    email: string
    password_hash?: string | null
    phone?: string | null
    is_organizer?: boolean | null
    is_sponsor?: boolean | null
    is_vendor?: boolean | null
    is_admin?: boolean | null
    is_active?: boolean | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
    events?: EventCreateNestedManyWithoutOrganizerInput
  }

  export type UserUncheckedCreateInput = {
    id?: number
    first_name?: string | null
    last_name?: string | null
    company_name?: string | null
    email: string
    password_hash?: string | null
    phone?: string | null
    is_organizer?: boolean | null
    is_sponsor?: boolean | null
    is_vendor?: boolean | null
    is_admin?: boolean | null
    is_active?: boolean | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
    events?: EventUncheckedCreateNestedManyWithoutOrganizerInput
  }

  export type UserUpdateInput = {
    first_name?: NullableStringFieldUpdateOperationsInput | string | null
    last_name?: NullableStringFieldUpdateOperationsInput | string | null
    company_name?: NullableStringFieldUpdateOperationsInput | string | null
    email?: StringFieldUpdateOperationsInput | string
    password_hash?: NullableStringFieldUpdateOperationsInput | string | null
    phone?: NullableStringFieldUpdateOperationsInput | string | null
    is_organizer?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_sponsor?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_vendor?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_admin?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_active?: NullableBoolFieldUpdateOperationsInput | boolean | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    events?: EventUpdateManyWithoutOrganizerNestedInput
  }

  export type UserUncheckedUpdateInput = {
    id?: IntFieldUpdateOperationsInput | number
    first_name?: NullableStringFieldUpdateOperationsInput | string | null
    last_name?: NullableStringFieldUpdateOperationsInput | string | null
    company_name?: NullableStringFieldUpdateOperationsInput | string | null
    email?: StringFieldUpdateOperationsInput | string
    password_hash?: NullableStringFieldUpdateOperationsInput | string | null
    phone?: NullableStringFieldUpdateOperationsInput | string | null
    is_organizer?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_sponsor?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_vendor?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_admin?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_active?: NullableBoolFieldUpdateOperationsInput | boolean | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    events?: EventUncheckedUpdateManyWithoutOrganizerNestedInput
  }

  export type UserCreateManyInput = {
    id?: number
    first_name?: string | null
    last_name?: string | null
    company_name?: string | null
    email: string
    password_hash?: string | null
    phone?: string | null
    is_organizer?: boolean | null
    is_sponsor?: boolean | null
    is_vendor?: boolean | null
    is_admin?: boolean | null
    is_active?: boolean | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
  }

  export type UserUpdateManyMutationInput = {
    first_name?: NullableStringFieldUpdateOperationsInput | string | null
    last_name?: NullableStringFieldUpdateOperationsInput | string | null
    company_name?: NullableStringFieldUpdateOperationsInput | string | null
    email?: StringFieldUpdateOperationsInput | string
    password_hash?: NullableStringFieldUpdateOperationsInput | string | null
    phone?: NullableStringFieldUpdateOperationsInput | string | null
    is_organizer?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_sponsor?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_vendor?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_admin?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_active?: NullableBoolFieldUpdateOperationsInput | boolean | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
  }

  export type UserUncheckedUpdateManyInput = {
    id?: IntFieldUpdateOperationsInput | number
    first_name?: NullableStringFieldUpdateOperationsInput | string | null
    last_name?: NullableStringFieldUpdateOperationsInput | string | null
    company_name?: NullableStringFieldUpdateOperationsInput | string | null
    email?: StringFieldUpdateOperationsInput | string
    password_hash?: NullableStringFieldUpdateOperationsInput | string | null
    phone?: NullableStringFieldUpdateOperationsInput | string | null
    is_organizer?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_sponsor?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_vendor?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_admin?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_active?: NullableBoolFieldUpdateOperationsInput | boolean | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
  }

  export type VenueCreateInput = {
    name?: string | null
    address?: string | null
    city?: string | null
    state?: string | null
    zip_code?: string | null
    latitude?: number | null
    longitude?: number | null
    capacity?: number | null
    venue_type_id?: number | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
    events?: EventCreateNestedManyWithoutVenueInput
  }

  export type VenueUncheckedCreateInput = {
    id?: number
    name?: string | null
    address?: string | null
    city?: string | null
    state?: string | null
    zip_code?: string | null
    latitude?: number | null
    longitude?: number | null
    capacity?: number | null
    venue_type_id?: number | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
    events?: EventUncheckedCreateNestedManyWithoutVenueInput
  }

  export type VenueUpdateInput = {
    name?: NullableStringFieldUpdateOperationsInput | string | null
    address?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zip_code?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    capacity?: NullableIntFieldUpdateOperationsInput | number | null
    venue_type_id?: NullableIntFieldUpdateOperationsInput | number | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    events?: EventUpdateManyWithoutVenueNestedInput
  }

  export type VenueUncheckedUpdateInput = {
    id?: IntFieldUpdateOperationsInput | number
    name?: NullableStringFieldUpdateOperationsInput | string | null
    address?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zip_code?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    capacity?: NullableIntFieldUpdateOperationsInput | number | null
    venue_type_id?: NullableIntFieldUpdateOperationsInput | number | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    events?: EventUncheckedUpdateManyWithoutVenueNestedInput
  }

  export type VenueCreateManyInput = {
    id?: number
    name?: string | null
    address?: string | null
    city?: string | null
    state?: string | null
    zip_code?: string | null
    latitude?: number | null
    longitude?: number | null
    capacity?: number | null
    venue_type_id?: number | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
  }

  export type VenueUpdateManyMutationInput = {
    name?: NullableStringFieldUpdateOperationsInput | string | null
    address?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zip_code?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    capacity?: NullableIntFieldUpdateOperationsInput | number | null
    venue_type_id?: NullableIntFieldUpdateOperationsInput | number | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
  }

  export type VenueUncheckedUpdateManyInput = {
    id?: IntFieldUpdateOperationsInput | number
    name?: NullableStringFieldUpdateOperationsInput | string | null
    address?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zip_code?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    capacity?: NullableIntFieldUpdateOperationsInput | number | null
    venue_type_id?: NullableIntFieldUpdateOperationsInput | number | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
  }

  export type FunalyticsScoreCreateInput = {
    id?: string
    communityVibe?: number | null
    familyFun?: number | null
    overallScore?: number | null
    reasoning?: string | null
    computedAt?: Date | string
    event: EventCreateNestedOneWithoutFunalyticsInput
  }

  export type FunalyticsScoreUncheckedCreateInput = {
    id?: string
    eventId: number
    communityVibe?: number | null
    familyFun?: number | null
    overallScore?: number | null
    reasoning?: string | null
    computedAt?: Date | string
  }

  export type FunalyticsScoreUpdateInput = {
    id?: StringFieldUpdateOperationsInput | string
    communityVibe?: NullableIntFieldUpdateOperationsInput | number | null
    familyFun?: NullableIntFieldUpdateOperationsInput | number | null
    overallScore?: NullableIntFieldUpdateOperationsInput | number | null
    reasoning?: NullableStringFieldUpdateOperationsInput | string | null
    computedAt?: DateTimeFieldUpdateOperationsInput | Date | string
    event?: EventUpdateOneRequiredWithoutFunalyticsNestedInput
  }

  export type FunalyticsScoreUncheckedUpdateInput = {
    id?: StringFieldUpdateOperationsInput | string
    eventId?: IntFieldUpdateOperationsInput | number
    communityVibe?: NullableIntFieldUpdateOperationsInput | number | null
    familyFun?: NullableIntFieldUpdateOperationsInput | number | null
    overallScore?: NullableIntFieldUpdateOperationsInput | number | null
    reasoning?: NullableStringFieldUpdateOperationsInput | string | null
    computedAt?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type FunalyticsScoreCreateManyInput = {
    id?: string
    eventId: number
    communityVibe?: number | null
    familyFun?: number | null
    overallScore?: number | null
    reasoning?: string | null
    computedAt?: Date | string
  }

  export type FunalyticsScoreUpdateManyMutationInput = {
    id?: StringFieldUpdateOperationsInput | string
    communityVibe?: NullableIntFieldUpdateOperationsInput | number | null
    familyFun?: NullableIntFieldUpdateOperationsInput | number | null
    overallScore?: NullableIntFieldUpdateOperationsInput | number | null
    reasoning?: NullableStringFieldUpdateOperationsInput | string | null
    computedAt?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type FunalyticsScoreUncheckedUpdateManyInput = {
    id?: StringFieldUpdateOperationsInput | string
    eventId?: IntFieldUpdateOperationsInput | number
    communityVibe?: NullableIntFieldUpdateOperationsInput | number | null
    familyFun?: NullableIntFieldUpdateOperationsInput | number | null
    overallScore?: NullableIntFieldUpdateOperationsInput | number | null
    reasoning?: NullableStringFieldUpdateOperationsInput | string | null
    computedAt?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type IntFilter<$PrismaModel = never> = {
    equals?: number | IntFieldRefInput<$PrismaModel>
    in?: number[] | ListIntFieldRefInput<$PrismaModel>
    notIn?: number[] | ListIntFieldRefInput<$PrismaModel>
    lt?: number | IntFieldRefInput<$PrismaModel>
    lte?: number | IntFieldRefInput<$PrismaModel>
    gt?: number | IntFieldRefInput<$PrismaModel>
    gte?: number | IntFieldRefInput<$PrismaModel>
    not?: NestedIntFilter<$PrismaModel> | number
  }

  export type StringFilter<$PrismaModel = never> = {
    equals?: string | StringFieldRefInput<$PrismaModel>
    in?: string[] | ListStringFieldRefInput<$PrismaModel>
    notIn?: string[] | ListStringFieldRefInput<$PrismaModel>
    lt?: string | StringFieldRefInput<$PrismaModel>
    lte?: string | StringFieldRefInput<$PrismaModel>
    gt?: string | StringFieldRefInput<$PrismaModel>
    gte?: string | StringFieldRefInput<$PrismaModel>
    contains?: string | StringFieldRefInput<$PrismaModel>
    startsWith?: string | StringFieldRefInput<$PrismaModel>
    endsWith?: string | StringFieldRefInput<$PrismaModel>
    mode?: QueryMode
    not?: NestedStringFilter<$PrismaModel> | string
  }

  export type StringNullableFilter<$PrismaModel = never> = {
    equals?: string | StringFieldRefInput<$PrismaModel> | null
    in?: string[] | ListStringFieldRefInput<$PrismaModel> | null
    notIn?: string[] | ListStringFieldRefInput<$PrismaModel> | null
    lt?: string | StringFieldRefInput<$PrismaModel>
    lte?: string | StringFieldRefInput<$PrismaModel>
    gt?: string | StringFieldRefInput<$PrismaModel>
    gte?: string | StringFieldRefInput<$PrismaModel>
    contains?: string | StringFieldRefInput<$PrismaModel>
    startsWith?: string | StringFieldRefInput<$PrismaModel>
    endsWith?: string | StringFieldRefInput<$PrismaModel>
    mode?: QueryMode
    not?: NestedStringNullableFilter<$PrismaModel> | string | null
  }

  export type DateTimeFilter<$PrismaModel = never> = {
    equals?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    in?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel>
    notIn?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel>
    lt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    lte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    not?: NestedDateTimeFilter<$PrismaModel> | Date | string
  }

  export type DateTimeNullableFilter<$PrismaModel = never> = {
    equals?: Date | string | DateTimeFieldRefInput<$PrismaModel> | null
    in?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel> | null
    notIn?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel> | null
    lt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    lte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    not?: NestedDateTimeNullableFilter<$PrismaModel> | Date | string | null
  }

  export type FloatNullableFilter<$PrismaModel = never> = {
    equals?: number | FloatFieldRefInput<$PrismaModel> | null
    in?: number[] | ListFloatFieldRefInput<$PrismaModel> | null
    notIn?: number[] | ListFloatFieldRefInput<$PrismaModel> | null
    lt?: number | FloatFieldRefInput<$PrismaModel>
    lte?: number | FloatFieldRefInput<$PrismaModel>
    gt?: number | FloatFieldRefInput<$PrismaModel>
    gte?: number | FloatFieldRefInput<$PrismaModel>
    not?: NestedFloatNullableFilter<$PrismaModel> | number | null
  }

  export type IntNullableFilter<$PrismaModel = never> = {
    equals?: number | IntFieldRefInput<$PrismaModel> | null
    in?: number[] | ListIntFieldRefInput<$PrismaModel> | null
    notIn?: number[] | ListIntFieldRefInput<$PrismaModel> | null
    lt?: number | IntFieldRefInput<$PrismaModel>
    lte?: number | IntFieldRefInput<$PrismaModel>
    gt?: number | IntFieldRefInput<$PrismaModel>
    gte?: number | IntFieldRefInput<$PrismaModel>
    not?: NestedIntNullableFilter<$PrismaModel> | number | null
  }

  export type UserNullableScalarRelationFilter = {
    is?: UserWhereInput | null
    isNot?: UserWhereInput | null
  }

  export type VenueNullableScalarRelationFilter = {
    is?: VenueWhereInput | null
    isNot?: VenueWhereInput | null
  }

  export type FunalyticsScoreListRelationFilter = {
    every?: FunalyticsScoreWhereInput
    some?: FunalyticsScoreWhereInput
    none?: FunalyticsScoreWhereInput
  }

  export type SortOrderInput = {
    sort: SortOrder
    nulls?: NullsOrder
  }

  export type FunalyticsScoreOrderByRelationAggregateInput = {
    _count?: SortOrder
  }

  export type EventCountOrderByAggregateInput = {
    id?: SortOrder
    title?: SortOrder
    description?: SortOrder
    startTime?: SortOrder
    endTime?: SortOrder
    location?: SortOrder
    city?: SortOrder
    state?: SortOrder
    zipCode?: SortOrder
    latitude?: SortOrder
    longitude?: SortOrder
    category?: SortOrder
    organizerId?: SortOrder
    venueId?: SortOrder
    status?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type EventAvgOrderByAggregateInput = {
    id?: SortOrder
    latitude?: SortOrder
    longitude?: SortOrder
    organizerId?: SortOrder
    venueId?: SortOrder
  }

  export type EventMaxOrderByAggregateInput = {
    id?: SortOrder
    title?: SortOrder
    description?: SortOrder
    startTime?: SortOrder
    endTime?: SortOrder
    location?: SortOrder
    city?: SortOrder
    state?: SortOrder
    zipCode?: SortOrder
    latitude?: SortOrder
    longitude?: SortOrder
    category?: SortOrder
    organizerId?: SortOrder
    venueId?: SortOrder
    status?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type EventMinOrderByAggregateInput = {
    id?: SortOrder
    title?: SortOrder
    description?: SortOrder
    startTime?: SortOrder
    endTime?: SortOrder
    location?: SortOrder
    city?: SortOrder
    state?: SortOrder
    zipCode?: SortOrder
    latitude?: SortOrder
    longitude?: SortOrder
    category?: SortOrder
    organizerId?: SortOrder
    venueId?: SortOrder
    status?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type EventSumOrderByAggregateInput = {
    id?: SortOrder
    latitude?: SortOrder
    longitude?: SortOrder
    organizerId?: SortOrder
    venueId?: SortOrder
  }

  export type IntWithAggregatesFilter<$PrismaModel = never> = {
    equals?: number | IntFieldRefInput<$PrismaModel>
    in?: number[] | ListIntFieldRefInput<$PrismaModel>
    notIn?: number[] | ListIntFieldRefInput<$PrismaModel>
    lt?: number | IntFieldRefInput<$PrismaModel>
    lte?: number | IntFieldRefInput<$PrismaModel>
    gt?: number | IntFieldRefInput<$PrismaModel>
    gte?: number | IntFieldRefInput<$PrismaModel>
    not?: NestedIntWithAggregatesFilter<$PrismaModel> | number
    _count?: NestedIntFilter<$PrismaModel>
    _avg?: NestedFloatFilter<$PrismaModel>
    _sum?: NestedIntFilter<$PrismaModel>
    _min?: NestedIntFilter<$PrismaModel>
    _max?: NestedIntFilter<$PrismaModel>
  }

  export type StringWithAggregatesFilter<$PrismaModel = never> = {
    equals?: string | StringFieldRefInput<$PrismaModel>
    in?: string[] | ListStringFieldRefInput<$PrismaModel>
    notIn?: string[] | ListStringFieldRefInput<$PrismaModel>
    lt?: string | StringFieldRefInput<$PrismaModel>
    lte?: string | StringFieldRefInput<$PrismaModel>
    gt?: string | StringFieldRefInput<$PrismaModel>
    gte?: string | StringFieldRefInput<$PrismaModel>
    contains?: string | StringFieldRefInput<$PrismaModel>
    startsWith?: string | StringFieldRefInput<$PrismaModel>
    endsWith?: string | StringFieldRefInput<$PrismaModel>
    mode?: QueryMode
    not?: NestedStringWithAggregatesFilter<$PrismaModel> | string
    _count?: NestedIntFilter<$PrismaModel>
    _min?: NestedStringFilter<$PrismaModel>
    _max?: NestedStringFilter<$PrismaModel>
  }

  export type StringNullableWithAggregatesFilter<$PrismaModel = never> = {
    equals?: string | StringFieldRefInput<$PrismaModel> | null
    in?: string[] | ListStringFieldRefInput<$PrismaModel> | null
    notIn?: string[] | ListStringFieldRefInput<$PrismaModel> | null
    lt?: string | StringFieldRefInput<$PrismaModel>
    lte?: string | StringFieldRefInput<$PrismaModel>
    gt?: string | StringFieldRefInput<$PrismaModel>
    gte?: string | StringFieldRefInput<$PrismaModel>
    contains?: string | StringFieldRefInput<$PrismaModel>
    startsWith?: string | StringFieldRefInput<$PrismaModel>
    endsWith?: string | StringFieldRefInput<$PrismaModel>
    mode?: QueryMode
    not?: NestedStringNullableWithAggregatesFilter<$PrismaModel> | string | null
    _count?: NestedIntNullableFilter<$PrismaModel>
    _min?: NestedStringNullableFilter<$PrismaModel>
    _max?: NestedStringNullableFilter<$PrismaModel>
  }

  export type DateTimeWithAggregatesFilter<$PrismaModel = never> = {
    equals?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    in?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel>
    notIn?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel>
    lt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    lte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    not?: NestedDateTimeWithAggregatesFilter<$PrismaModel> | Date | string
    _count?: NestedIntFilter<$PrismaModel>
    _min?: NestedDateTimeFilter<$PrismaModel>
    _max?: NestedDateTimeFilter<$PrismaModel>
  }

  export type DateTimeNullableWithAggregatesFilter<$PrismaModel = never> = {
    equals?: Date | string | DateTimeFieldRefInput<$PrismaModel> | null
    in?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel> | null
    notIn?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel> | null
    lt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    lte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    not?: NestedDateTimeNullableWithAggregatesFilter<$PrismaModel> | Date | string | null
    _count?: NestedIntNullableFilter<$PrismaModel>
    _min?: NestedDateTimeNullableFilter<$PrismaModel>
    _max?: NestedDateTimeNullableFilter<$PrismaModel>
  }

  export type FloatNullableWithAggregatesFilter<$PrismaModel = never> = {
    equals?: number | FloatFieldRefInput<$PrismaModel> | null
    in?: number[] | ListFloatFieldRefInput<$PrismaModel> | null
    notIn?: number[] | ListFloatFieldRefInput<$PrismaModel> | null
    lt?: number | FloatFieldRefInput<$PrismaModel>
    lte?: number | FloatFieldRefInput<$PrismaModel>
    gt?: number | FloatFieldRefInput<$PrismaModel>
    gte?: number | FloatFieldRefInput<$PrismaModel>
    not?: NestedFloatNullableWithAggregatesFilter<$PrismaModel> | number | null
    _count?: NestedIntNullableFilter<$PrismaModel>
    _avg?: NestedFloatNullableFilter<$PrismaModel>
    _sum?: NestedFloatNullableFilter<$PrismaModel>
    _min?: NestedFloatNullableFilter<$PrismaModel>
    _max?: NestedFloatNullableFilter<$PrismaModel>
  }

  export type IntNullableWithAggregatesFilter<$PrismaModel = never> = {
    equals?: number | IntFieldRefInput<$PrismaModel> | null
    in?: number[] | ListIntFieldRefInput<$PrismaModel> | null
    notIn?: number[] | ListIntFieldRefInput<$PrismaModel> | null
    lt?: number | IntFieldRefInput<$PrismaModel>
    lte?: number | IntFieldRefInput<$PrismaModel>
    gt?: number | IntFieldRefInput<$PrismaModel>
    gte?: number | IntFieldRefInput<$PrismaModel>
    not?: NestedIntNullableWithAggregatesFilter<$PrismaModel> | number | null
    _count?: NestedIntNullableFilter<$PrismaModel>
    _avg?: NestedFloatNullableFilter<$PrismaModel>
    _sum?: NestedIntNullableFilter<$PrismaModel>
    _min?: NestedIntNullableFilter<$PrismaModel>
    _max?: NestedIntNullableFilter<$PrismaModel>
  }

  export type BoolNullableFilter<$PrismaModel = never> = {
    equals?: boolean | BooleanFieldRefInput<$PrismaModel> | null
    not?: NestedBoolNullableFilter<$PrismaModel> | boolean | null
  }

  export type EventListRelationFilter = {
    every?: EventWhereInput
    some?: EventWhereInput
    none?: EventWhereInput
  }

  export type EventOrderByRelationAggregateInput = {
    _count?: SortOrder
  }

  export type UserCountOrderByAggregateInput = {
    id?: SortOrder
    first_name?: SortOrder
    last_name?: SortOrder
    company_name?: SortOrder
    email?: SortOrder
    password_hash?: SortOrder
    phone?: SortOrder
    is_organizer?: SortOrder
    is_sponsor?: SortOrder
    is_vendor?: SortOrder
    is_admin?: SortOrder
    is_active?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type UserAvgOrderByAggregateInput = {
    id?: SortOrder
  }

  export type UserMaxOrderByAggregateInput = {
    id?: SortOrder
    first_name?: SortOrder
    last_name?: SortOrder
    company_name?: SortOrder
    email?: SortOrder
    password_hash?: SortOrder
    phone?: SortOrder
    is_organizer?: SortOrder
    is_sponsor?: SortOrder
    is_vendor?: SortOrder
    is_admin?: SortOrder
    is_active?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type UserMinOrderByAggregateInput = {
    id?: SortOrder
    first_name?: SortOrder
    last_name?: SortOrder
    company_name?: SortOrder
    email?: SortOrder
    password_hash?: SortOrder
    phone?: SortOrder
    is_organizer?: SortOrder
    is_sponsor?: SortOrder
    is_vendor?: SortOrder
    is_admin?: SortOrder
    is_active?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type UserSumOrderByAggregateInput = {
    id?: SortOrder
  }

  export type BoolNullableWithAggregatesFilter<$PrismaModel = never> = {
    equals?: boolean | BooleanFieldRefInput<$PrismaModel> | null
    not?: NestedBoolNullableWithAggregatesFilter<$PrismaModel> | boolean | null
    _count?: NestedIntNullableFilter<$PrismaModel>
    _min?: NestedBoolNullableFilter<$PrismaModel>
    _max?: NestedBoolNullableFilter<$PrismaModel>
  }

  export type VenueCountOrderByAggregateInput = {
    id?: SortOrder
    name?: SortOrder
    address?: SortOrder
    city?: SortOrder
    state?: SortOrder
    zip_code?: SortOrder
    latitude?: SortOrder
    longitude?: SortOrder
    capacity?: SortOrder
    venue_type_id?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type VenueAvgOrderByAggregateInput = {
    id?: SortOrder
    latitude?: SortOrder
    longitude?: SortOrder
    capacity?: SortOrder
    venue_type_id?: SortOrder
  }

  export type VenueMaxOrderByAggregateInput = {
    id?: SortOrder
    name?: SortOrder
    address?: SortOrder
    city?: SortOrder
    state?: SortOrder
    zip_code?: SortOrder
    latitude?: SortOrder
    longitude?: SortOrder
    capacity?: SortOrder
    venue_type_id?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type VenueMinOrderByAggregateInput = {
    id?: SortOrder
    name?: SortOrder
    address?: SortOrder
    city?: SortOrder
    state?: SortOrder
    zip_code?: SortOrder
    latitude?: SortOrder
    longitude?: SortOrder
    capacity?: SortOrder
    venue_type_id?: SortOrder
    created_at?: SortOrder
    updated_at?: SortOrder
  }

  export type VenueSumOrderByAggregateInput = {
    id?: SortOrder
    latitude?: SortOrder
    longitude?: SortOrder
    capacity?: SortOrder
    venue_type_id?: SortOrder
  }

  export type EventScalarRelationFilter = {
    is?: EventWhereInput
    isNot?: EventWhereInput
  }

  export type FunalyticsScoreCountOrderByAggregateInput = {
    id?: SortOrder
    eventId?: SortOrder
    communityVibe?: SortOrder
    familyFun?: SortOrder
    overallScore?: SortOrder
    reasoning?: SortOrder
    computedAt?: SortOrder
  }

  export type FunalyticsScoreAvgOrderByAggregateInput = {
    eventId?: SortOrder
    communityVibe?: SortOrder
    familyFun?: SortOrder
    overallScore?: SortOrder
  }

  export type FunalyticsScoreMaxOrderByAggregateInput = {
    id?: SortOrder
    eventId?: SortOrder
    communityVibe?: SortOrder
    familyFun?: SortOrder
    overallScore?: SortOrder
    reasoning?: SortOrder
    computedAt?: SortOrder
  }

  export type FunalyticsScoreMinOrderByAggregateInput = {
    id?: SortOrder
    eventId?: SortOrder
    communityVibe?: SortOrder
    familyFun?: SortOrder
    overallScore?: SortOrder
    reasoning?: SortOrder
    computedAt?: SortOrder
  }

  export type FunalyticsScoreSumOrderByAggregateInput = {
    eventId?: SortOrder
    communityVibe?: SortOrder
    familyFun?: SortOrder
    overallScore?: SortOrder
  }

  export type UserCreateNestedOneWithoutEventsInput = {
    create?: XOR<UserCreateWithoutEventsInput, UserUncheckedCreateWithoutEventsInput>
    connectOrCreate?: UserCreateOrConnectWithoutEventsInput
    connect?: UserWhereUniqueInput
  }

  export type VenueCreateNestedOneWithoutEventsInput = {
    create?: XOR<VenueCreateWithoutEventsInput, VenueUncheckedCreateWithoutEventsInput>
    connectOrCreate?: VenueCreateOrConnectWithoutEventsInput
    connect?: VenueWhereUniqueInput
  }

  export type FunalyticsScoreCreateNestedManyWithoutEventInput = {
    create?: XOR<FunalyticsScoreCreateWithoutEventInput, FunalyticsScoreUncheckedCreateWithoutEventInput> | FunalyticsScoreCreateWithoutEventInput[] | FunalyticsScoreUncheckedCreateWithoutEventInput[]
    connectOrCreate?: FunalyticsScoreCreateOrConnectWithoutEventInput | FunalyticsScoreCreateOrConnectWithoutEventInput[]
    createMany?: FunalyticsScoreCreateManyEventInputEnvelope
    connect?: FunalyticsScoreWhereUniqueInput | FunalyticsScoreWhereUniqueInput[]
  }

  export type FunalyticsScoreUncheckedCreateNestedManyWithoutEventInput = {
    create?: XOR<FunalyticsScoreCreateWithoutEventInput, FunalyticsScoreUncheckedCreateWithoutEventInput> | FunalyticsScoreCreateWithoutEventInput[] | FunalyticsScoreUncheckedCreateWithoutEventInput[]
    connectOrCreate?: FunalyticsScoreCreateOrConnectWithoutEventInput | FunalyticsScoreCreateOrConnectWithoutEventInput[]
    createMany?: FunalyticsScoreCreateManyEventInputEnvelope
    connect?: FunalyticsScoreWhereUniqueInput | FunalyticsScoreWhereUniqueInput[]
  }

  export type StringFieldUpdateOperationsInput = {
    set?: string
  }

  export type NullableStringFieldUpdateOperationsInput = {
    set?: string | null
  }

  export type DateTimeFieldUpdateOperationsInput = {
    set?: Date | string
  }

  export type NullableDateTimeFieldUpdateOperationsInput = {
    set?: Date | string | null
  }

  export type NullableFloatFieldUpdateOperationsInput = {
    set?: number | null
    increment?: number
    decrement?: number
    multiply?: number
    divide?: number
  }

  export type UserUpdateOneWithoutEventsNestedInput = {
    create?: XOR<UserCreateWithoutEventsInput, UserUncheckedCreateWithoutEventsInput>
    connectOrCreate?: UserCreateOrConnectWithoutEventsInput
    upsert?: UserUpsertWithoutEventsInput
    disconnect?: UserWhereInput | boolean
    delete?: UserWhereInput | boolean
    connect?: UserWhereUniqueInput
    update?: XOR<XOR<UserUpdateToOneWithWhereWithoutEventsInput, UserUpdateWithoutEventsInput>, UserUncheckedUpdateWithoutEventsInput>
  }

  export type VenueUpdateOneWithoutEventsNestedInput = {
    create?: XOR<VenueCreateWithoutEventsInput, VenueUncheckedCreateWithoutEventsInput>
    connectOrCreate?: VenueCreateOrConnectWithoutEventsInput
    upsert?: VenueUpsertWithoutEventsInput
    disconnect?: VenueWhereInput | boolean
    delete?: VenueWhereInput | boolean
    connect?: VenueWhereUniqueInput
    update?: XOR<XOR<VenueUpdateToOneWithWhereWithoutEventsInput, VenueUpdateWithoutEventsInput>, VenueUncheckedUpdateWithoutEventsInput>
  }

  export type FunalyticsScoreUpdateManyWithoutEventNestedInput = {
    create?: XOR<FunalyticsScoreCreateWithoutEventInput, FunalyticsScoreUncheckedCreateWithoutEventInput> | FunalyticsScoreCreateWithoutEventInput[] | FunalyticsScoreUncheckedCreateWithoutEventInput[]
    connectOrCreate?: FunalyticsScoreCreateOrConnectWithoutEventInput | FunalyticsScoreCreateOrConnectWithoutEventInput[]
    upsert?: FunalyticsScoreUpsertWithWhereUniqueWithoutEventInput | FunalyticsScoreUpsertWithWhereUniqueWithoutEventInput[]
    createMany?: FunalyticsScoreCreateManyEventInputEnvelope
    set?: FunalyticsScoreWhereUniqueInput | FunalyticsScoreWhereUniqueInput[]
    disconnect?: FunalyticsScoreWhereUniqueInput | FunalyticsScoreWhereUniqueInput[]
    delete?: FunalyticsScoreWhereUniqueInput | FunalyticsScoreWhereUniqueInput[]
    connect?: FunalyticsScoreWhereUniqueInput | FunalyticsScoreWhereUniqueInput[]
    update?: FunalyticsScoreUpdateWithWhereUniqueWithoutEventInput | FunalyticsScoreUpdateWithWhereUniqueWithoutEventInput[]
    updateMany?: FunalyticsScoreUpdateManyWithWhereWithoutEventInput | FunalyticsScoreUpdateManyWithWhereWithoutEventInput[]
    deleteMany?: FunalyticsScoreScalarWhereInput | FunalyticsScoreScalarWhereInput[]
  }

  export type IntFieldUpdateOperationsInput = {
    set?: number
    increment?: number
    decrement?: number
    multiply?: number
    divide?: number
  }

  export type NullableIntFieldUpdateOperationsInput = {
    set?: number | null
    increment?: number
    decrement?: number
    multiply?: number
    divide?: number
  }

  export type FunalyticsScoreUncheckedUpdateManyWithoutEventNestedInput = {
    create?: XOR<FunalyticsScoreCreateWithoutEventInput, FunalyticsScoreUncheckedCreateWithoutEventInput> | FunalyticsScoreCreateWithoutEventInput[] | FunalyticsScoreUncheckedCreateWithoutEventInput[]
    connectOrCreate?: FunalyticsScoreCreateOrConnectWithoutEventInput | FunalyticsScoreCreateOrConnectWithoutEventInput[]
    upsert?: FunalyticsScoreUpsertWithWhereUniqueWithoutEventInput | FunalyticsScoreUpsertWithWhereUniqueWithoutEventInput[]
    createMany?: FunalyticsScoreCreateManyEventInputEnvelope
    set?: FunalyticsScoreWhereUniqueInput | FunalyticsScoreWhereUniqueInput[]
    disconnect?: FunalyticsScoreWhereUniqueInput | FunalyticsScoreWhereUniqueInput[]
    delete?: FunalyticsScoreWhereUniqueInput | FunalyticsScoreWhereUniqueInput[]
    connect?: FunalyticsScoreWhereUniqueInput | FunalyticsScoreWhereUniqueInput[]
    update?: FunalyticsScoreUpdateWithWhereUniqueWithoutEventInput | FunalyticsScoreUpdateWithWhereUniqueWithoutEventInput[]
    updateMany?: FunalyticsScoreUpdateManyWithWhereWithoutEventInput | FunalyticsScoreUpdateManyWithWhereWithoutEventInput[]
    deleteMany?: FunalyticsScoreScalarWhereInput | FunalyticsScoreScalarWhereInput[]
  }

  export type EventCreateNestedManyWithoutOrganizerInput = {
    create?: XOR<EventCreateWithoutOrganizerInput, EventUncheckedCreateWithoutOrganizerInput> | EventCreateWithoutOrganizerInput[] | EventUncheckedCreateWithoutOrganizerInput[]
    connectOrCreate?: EventCreateOrConnectWithoutOrganizerInput | EventCreateOrConnectWithoutOrganizerInput[]
    createMany?: EventCreateManyOrganizerInputEnvelope
    connect?: EventWhereUniqueInput | EventWhereUniqueInput[]
  }

  export type EventUncheckedCreateNestedManyWithoutOrganizerInput = {
    create?: XOR<EventCreateWithoutOrganizerInput, EventUncheckedCreateWithoutOrganizerInput> | EventCreateWithoutOrganizerInput[] | EventUncheckedCreateWithoutOrganizerInput[]
    connectOrCreate?: EventCreateOrConnectWithoutOrganizerInput | EventCreateOrConnectWithoutOrganizerInput[]
    createMany?: EventCreateManyOrganizerInputEnvelope
    connect?: EventWhereUniqueInput | EventWhereUniqueInput[]
  }

  export type NullableBoolFieldUpdateOperationsInput = {
    set?: boolean | null
  }

  export type EventUpdateManyWithoutOrganizerNestedInput = {
    create?: XOR<EventCreateWithoutOrganizerInput, EventUncheckedCreateWithoutOrganizerInput> | EventCreateWithoutOrganizerInput[] | EventUncheckedCreateWithoutOrganizerInput[]
    connectOrCreate?: EventCreateOrConnectWithoutOrganizerInput | EventCreateOrConnectWithoutOrganizerInput[]
    upsert?: EventUpsertWithWhereUniqueWithoutOrganizerInput | EventUpsertWithWhereUniqueWithoutOrganizerInput[]
    createMany?: EventCreateManyOrganizerInputEnvelope
    set?: EventWhereUniqueInput | EventWhereUniqueInput[]
    disconnect?: EventWhereUniqueInput | EventWhereUniqueInput[]
    delete?: EventWhereUniqueInput | EventWhereUniqueInput[]
    connect?: EventWhereUniqueInput | EventWhereUniqueInput[]
    update?: EventUpdateWithWhereUniqueWithoutOrganizerInput | EventUpdateWithWhereUniqueWithoutOrganizerInput[]
    updateMany?: EventUpdateManyWithWhereWithoutOrganizerInput | EventUpdateManyWithWhereWithoutOrganizerInput[]
    deleteMany?: EventScalarWhereInput | EventScalarWhereInput[]
  }

  export type EventUncheckedUpdateManyWithoutOrganizerNestedInput = {
    create?: XOR<EventCreateWithoutOrganizerInput, EventUncheckedCreateWithoutOrganizerInput> | EventCreateWithoutOrganizerInput[] | EventUncheckedCreateWithoutOrganizerInput[]
    connectOrCreate?: EventCreateOrConnectWithoutOrganizerInput | EventCreateOrConnectWithoutOrganizerInput[]
    upsert?: EventUpsertWithWhereUniqueWithoutOrganizerInput | EventUpsertWithWhereUniqueWithoutOrganizerInput[]
    createMany?: EventCreateManyOrganizerInputEnvelope
    set?: EventWhereUniqueInput | EventWhereUniqueInput[]
    disconnect?: EventWhereUniqueInput | EventWhereUniqueInput[]
    delete?: EventWhereUniqueInput | EventWhereUniqueInput[]
    connect?: EventWhereUniqueInput | EventWhereUniqueInput[]
    update?: EventUpdateWithWhereUniqueWithoutOrganizerInput | EventUpdateWithWhereUniqueWithoutOrganizerInput[]
    updateMany?: EventUpdateManyWithWhereWithoutOrganizerInput | EventUpdateManyWithWhereWithoutOrganizerInput[]
    deleteMany?: EventScalarWhereInput | EventScalarWhereInput[]
  }

  export type EventCreateNestedManyWithoutVenueInput = {
    create?: XOR<EventCreateWithoutVenueInput, EventUncheckedCreateWithoutVenueInput> | EventCreateWithoutVenueInput[] | EventUncheckedCreateWithoutVenueInput[]
    connectOrCreate?: EventCreateOrConnectWithoutVenueInput | EventCreateOrConnectWithoutVenueInput[]
    createMany?: EventCreateManyVenueInputEnvelope
    connect?: EventWhereUniqueInput | EventWhereUniqueInput[]
  }

  export type EventUncheckedCreateNestedManyWithoutVenueInput = {
    create?: XOR<EventCreateWithoutVenueInput, EventUncheckedCreateWithoutVenueInput> | EventCreateWithoutVenueInput[] | EventUncheckedCreateWithoutVenueInput[]
    connectOrCreate?: EventCreateOrConnectWithoutVenueInput | EventCreateOrConnectWithoutVenueInput[]
    createMany?: EventCreateManyVenueInputEnvelope
    connect?: EventWhereUniqueInput | EventWhereUniqueInput[]
  }

  export type EventUpdateManyWithoutVenueNestedInput = {
    create?: XOR<EventCreateWithoutVenueInput, EventUncheckedCreateWithoutVenueInput> | EventCreateWithoutVenueInput[] | EventUncheckedCreateWithoutVenueInput[]
    connectOrCreate?: EventCreateOrConnectWithoutVenueInput | EventCreateOrConnectWithoutVenueInput[]
    upsert?: EventUpsertWithWhereUniqueWithoutVenueInput | EventUpsertWithWhereUniqueWithoutVenueInput[]
    createMany?: EventCreateManyVenueInputEnvelope
    set?: EventWhereUniqueInput | EventWhereUniqueInput[]
    disconnect?: EventWhereUniqueInput | EventWhereUniqueInput[]
    delete?: EventWhereUniqueInput | EventWhereUniqueInput[]
    connect?: EventWhereUniqueInput | EventWhereUniqueInput[]
    update?: EventUpdateWithWhereUniqueWithoutVenueInput | EventUpdateWithWhereUniqueWithoutVenueInput[]
    updateMany?: EventUpdateManyWithWhereWithoutVenueInput | EventUpdateManyWithWhereWithoutVenueInput[]
    deleteMany?: EventScalarWhereInput | EventScalarWhereInput[]
  }

  export type EventUncheckedUpdateManyWithoutVenueNestedInput = {
    create?: XOR<EventCreateWithoutVenueInput, EventUncheckedCreateWithoutVenueInput> | EventCreateWithoutVenueInput[] | EventUncheckedCreateWithoutVenueInput[]
    connectOrCreate?: EventCreateOrConnectWithoutVenueInput | EventCreateOrConnectWithoutVenueInput[]
    upsert?: EventUpsertWithWhereUniqueWithoutVenueInput | EventUpsertWithWhereUniqueWithoutVenueInput[]
    createMany?: EventCreateManyVenueInputEnvelope
    set?: EventWhereUniqueInput | EventWhereUniqueInput[]
    disconnect?: EventWhereUniqueInput | EventWhereUniqueInput[]
    delete?: EventWhereUniqueInput | EventWhereUniqueInput[]
    connect?: EventWhereUniqueInput | EventWhereUniqueInput[]
    update?: EventUpdateWithWhereUniqueWithoutVenueInput | EventUpdateWithWhereUniqueWithoutVenueInput[]
    updateMany?: EventUpdateManyWithWhereWithoutVenueInput | EventUpdateManyWithWhereWithoutVenueInput[]
    deleteMany?: EventScalarWhereInput | EventScalarWhereInput[]
  }

  export type EventCreateNestedOneWithoutFunalyticsInput = {
    create?: XOR<EventCreateWithoutFunalyticsInput, EventUncheckedCreateWithoutFunalyticsInput>
    connectOrCreate?: EventCreateOrConnectWithoutFunalyticsInput
    connect?: EventWhereUniqueInput
  }

  export type EventUpdateOneRequiredWithoutFunalyticsNestedInput = {
    create?: XOR<EventCreateWithoutFunalyticsInput, EventUncheckedCreateWithoutFunalyticsInput>
    connectOrCreate?: EventCreateOrConnectWithoutFunalyticsInput
    upsert?: EventUpsertWithoutFunalyticsInput
    connect?: EventWhereUniqueInput
    update?: XOR<XOR<EventUpdateToOneWithWhereWithoutFunalyticsInput, EventUpdateWithoutFunalyticsInput>, EventUncheckedUpdateWithoutFunalyticsInput>
  }

  export type NestedIntFilter<$PrismaModel = never> = {
    equals?: number | IntFieldRefInput<$PrismaModel>
    in?: number[] | ListIntFieldRefInput<$PrismaModel>
    notIn?: number[] | ListIntFieldRefInput<$PrismaModel>
    lt?: number | IntFieldRefInput<$PrismaModel>
    lte?: number | IntFieldRefInput<$PrismaModel>
    gt?: number | IntFieldRefInput<$PrismaModel>
    gte?: number | IntFieldRefInput<$PrismaModel>
    not?: NestedIntFilter<$PrismaModel> | number
  }

  export type NestedStringFilter<$PrismaModel = never> = {
    equals?: string | StringFieldRefInput<$PrismaModel>
    in?: string[] | ListStringFieldRefInput<$PrismaModel>
    notIn?: string[] | ListStringFieldRefInput<$PrismaModel>
    lt?: string | StringFieldRefInput<$PrismaModel>
    lte?: string | StringFieldRefInput<$PrismaModel>
    gt?: string | StringFieldRefInput<$PrismaModel>
    gte?: string | StringFieldRefInput<$PrismaModel>
    contains?: string | StringFieldRefInput<$PrismaModel>
    startsWith?: string | StringFieldRefInput<$PrismaModel>
    endsWith?: string | StringFieldRefInput<$PrismaModel>
    not?: NestedStringFilter<$PrismaModel> | string
  }

  export type NestedStringNullableFilter<$PrismaModel = never> = {
    equals?: string | StringFieldRefInput<$PrismaModel> | null
    in?: string[] | ListStringFieldRefInput<$PrismaModel> | null
    notIn?: string[] | ListStringFieldRefInput<$PrismaModel> | null
    lt?: string | StringFieldRefInput<$PrismaModel>
    lte?: string | StringFieldRefInput<$PrismaModel>
    gt?: string | StringFieldRefInput<$PrismaModel>
    gte?: string | StringFieldRefInput<$PrismaModel>
    contains?: string | StringFieldRefInput<$PrismaModel>
    startsWith?: string | StringFieldRefInput<$PrismaModel>
    endsWith?: string | StringFieldRefInput<$PrismaModel>
    not?: NestedStringNullableFilter<$PrismaModel> | string | null
  }

  export type NestedDateTimeFilter<$PrismaModel = never> = {
    equals?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    in?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel>
    notIn?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel>
    lt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    lte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    not?: NestedDateTimeFilter<$PrismaModel> | Date | string
  }

  export type NestedDateTimeNullableFilter<$PrismaModel = never> = {
    equals?: Date | string | DateTimeFieldRefInput<$PrismaModel> | null
    in?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel> | null
    notIn?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel> | null
    lt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    lte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    not?: NestedDateTimeNullableFilter<$PrismaModel> | Date | string | null
  }

  export type NestedFloatNullableFilter<$PrismaModel = never> = {
    equals?: number | FloatFieldRefInput<$PrismaModel> | null
    in?: number[] | ListFloatFieldRefInput<$PrismaModel> | null
    notIn?: number[] | ListFloatFieldRefInput<$PrismaModel> | null
    lt?: number | FloatFieldRefInput<$PrismaModel>
    lte?: number | FloatFieldRefInput<$PrismaModel>
    gt?: number | FloatFieldRefInput<$PrismaModel>
    gte?: number | FloatFieldRefInput<$PrismaModel>
    not?: NestedFloatNullableFilter<$PrismaModel> | number | null
  }

  export type NestedIntNullableFilter<$PrismaModel = never> = {
    equals?: number | IntFieldRefInput<$PrismaModel> | null
    in?: number[] | ListIntFieldRefInput<$PrismaModel> | null
    notIn?: number[] | ListIntFieldRefInput<$PrismaModel> | null
    lt?: number | IntFieldRefInput<$PrismaModel>
    lte?: number | IntFieldRefInput<$PrismaModel>
    gt?: number | IntFieldRefInput<$PrismaModel>
    gte?: number | IntFieldRefInput<$PrismaModel>
    not?: NestedIntNullableFilter<$PrismaModel> | number | null
  }

  export type NestedIntWithAggregatesFilter<$PrismaModel = never> = {
    equals?: number | IntFieldRefInput<$PrismaModel>
    in?: number[] | ListIntFieldRefInput<$PrismaModel>
    notIn?: number[] | ListIntFieldRefInput<$PrismaModel>
    lt?: number | IntFieldRefInput<$PrismaModel>
    lte?: number | IntFieldRefInput<$PrismaModel>
    gt?: number | IntFieldRefInput<$PrismaModel>
    gte?: number | IntFieldRefInput<$PrismaModel>
    not?: NestedIntWithAggregatesFilter<$PrismaModel> | number
    _count?: NestedIntFilter<$PrismaModel>
    _avg?: NestedFloatFilter<$PrismaModel>
    _sum?: NestedIntFilter<$PrismaModel>
    _min?: NestedIntFilter<$PrismaModel>
    _max?: NestedIntFilter<$PrismaModel>
  }

  export type NestedFloatFilter<$PrismaModel = never> = {
    equals?: number | FloatFieldRefInput<$PrismaModel>
    in?: number[] | ListFloatFieldRefInput<$PrismaModel>
    notIn?: number[] | ListFloatFieldRefInput<$PrismaModel>
    lt?: number | FloatFieldRefInput<$PrismaModel>
    lte?: number | FloatFieldRefInput<$PrismaModel>
    gt?: number | FloatFieldRefInput<$PrismaModel>
    gte?: number | FloatFieldRefInput<$PrismaModel>
    not?: NestedFloatFilter<$PrismaModel> | number
  }

  export type NestedStringWithAggregatesFilter<$PrismaModel = never> = {
    equals?: string | StringFieldRefInput<$PrismaModel>
    in?: string[] | ListStringFieldRefInput<$PrismaModel>
    notIn?: string[] | ListStringFieldRefInput<$PrismaModel>
    lt?: string | StringFieldRefInput<$PrismaModel>
    lte?: string | StringFieldRefInput<$PrismaModel>
    gt?: string | StringFieldRefInput<$PrismaModel>
    gte?: string | StringFieldRefInput<$PrismaModel>
    contains?: string | StringFieldRefInput<$PrismaModel>
    startsWith?: string | StringFieldRefInput<$PrismaModel>
    endsWith?: string | StringFieldRefInput<$PrismaModel>
    not?: NestedStringWithAggregatesFilter<$PrismaModel> | string
    _count?: NestedIntFilter<$PrismaModel>
    _min?: NestedStringFilter<$PrismaModel>
    _max?: NestedStringFilter<$PrismaModel>
  }

  export type NestedStringNullableWithAggregatesFilter<$PrismaModel = never> = {
    equals?: string | StringFieldRefInput<$PrismaModel> | null
    in?: string[] | ListStringFieldRefInput<$PrismaModel> | null
    notIn?: string[] | ListStringFieldRefInput<$PrismaModel> | null
    lt?: string | StringFieldRefInput<$PrismaModel>
    lte?: string | StringFieldRefInput<$PrismaModel>
    gt?: string | StringFieldRefInput<$PrismaModel>
    gte?: string | StringFieldRefInput<$PrismaModel>
    contains?: string | StringFieldRefInput<$PrismaModel>
    startsWith?: string | StringFieldRefInput<$PrismaModel>
    endsWith?: string | StringFieldRefInput<$PrismaModel>
    not?: NestedStringNullableWithAggregatesFilter<$PrismaModel> | string | null
    _count?: NestedIntNullableFilter<$PrismaModel>
    _min?: NestedStringNullableFilter<$PrismaModel>
    _max?: NestedStringNullableFilter<$PrismaModel>
  }

  export type NestedDateTimeWithAggregatesFilter<$PrismaModel = never> = {
    equals?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    in?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel>
    notIn?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel>
    lt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    lte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    not?: NestedDateTimeWithAggregatesFilter<$PrismaModel> | Date | string
    _count?: NestedIntFilter<$PrismaModel>
    _min?: NestedDateTimeFilter<$PrismaModel>
    _max?: NestedDateTimeFilter<$PrismaModel>
  }

  export type NestedDateTimeNullableWithAggregatesFilter<$PrismaModel = never> = {
    equals?: Date | string | DateTimeFieldRefInput<$PrismaModel> | null
    in?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel> | null
    notIn?: Date[] | string[] | ListDateTimeFieldRefInput<$PrismaModel> | null
    lt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    lte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gt?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    gte?: Date | string | DateTimeFieldRefInput<$PrismaModel>
    not?: NestedDateTimeNullableWithAggregatesFilter<$PrismaModel> | Date | string | null
    _count?: NestedIntNullableFilter<$PrismaModel>
    _min?: NestedDateTimeNullableFilter<$PrismaModel>
    _max?: NestedDateTimeNullableFilter<$PrismaModel>
  }

  export type NestedFloatNullableWithAggregatesFilter<$PrismaModel = never> = {
    equals?: number | FloatFieldRefInput<$PrismaModel> | null
    in?: number[] | ListFloatFieldRefInput<$PrismaModel> | null
    notIn?: number[] | ListFloatFieldRefInput<$PrismaModel> | null
    lt?: number | FloatFieldRefInput<$PrismaModel>
    lte?: number | FloatFieldRefInput<$PrismaModel>
    gt?: number | FloatFieldRefInput<$PrismaModel>
    gte?: number | FloatFieldRefInput<$PrismaModel>
    not?: NestedFloatNullableWithAggregatesFilter<$PrismaModel> | number | null
    _count?: NestedIntNullableFilter<$PrismaModel>
    _avg?: NestedFloatNullableFilter<$PrismaModel>
    _sum?: NestedFloatNullableFilter<$PrismaModel>
    _min?: NestedFloatNullableFilter<$PrismaModel>
    _max?: NestedFloatNullableFilter<$PrismaModel>
  }

  export type NestedIntNullableWithAggregatesFilter<$PrismaModel = never> = {
    equals?: number | IntFieldRefInput<$PrismaModel> | null
    in?: number[] | ListIntFieldRefInput<$PrismaModel> | null
    notIn?: number[] | ListIntFieldRefInput<$PrismaModel> | null
    lt?: number | IntFieldRefInput<$PrismaModel>
    lte?: number | IntFieldRefInput<$PrismaModel>
    gt?: number | IntFieldRefInput<$PrismaModel>
    gte?: number | IntFieldRefInput<$PrismaModel>
    not?: NestedIntNullableWithAggregatesFilter<$PrismaModel> | number | null
    _count?: NestedIntNullableFilter<$PrismaModel>
    _avg?: NestedFloatNullableFilter<$PrismaModel>
    _sum?: NestedIntNullableFilter<$PrismaModel>
    _min?: NestedIntNullableFilter<$PrismaModel>
    _max?: NestedIntNullableFilter<$PrismaModel>
  }

  export type NestedBoolNullableFilter<$PrismaModel = never> = {
    equals?: boolean | BooleanFieldRefInput<$PrismaModel> | null
    not?: NestedBoolNullableFilter<$PrismaModel> | boolean | null
  }

  export type NestedBoolNullableWithAggregatesFilter<$PrismaModel = never> = {
    equals?: boolean | BooleanFieldRefInput<$PrismaModel> | null
    not?: NestedBoolNullableWithAggregatesFilter<$PrismaModel> | boolean | null
    _count?: NestedIntNullableFilter<$PrismaModel>
    _min?: NestedBoolNullableFilter<$PrismaModel>
    _max?: NestedBoolNullableFilter<$PrismaModel>
  }

  export type UserCreateWithoutEventsInput = {
    first_name?: string | null
    last_name?: string | null
    company_name?: string | null
    email: string
    password_hash?: string | null
    phone?: string | null
    is_organizer?: boolean | null
    is_sponsor?: boolean | null
    is_vendor?: boolean | null
    is_admin?: boolean | null
    is_active?: boolean | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
  }

  export type UserUncheckedCreateWithoutEventsInput = {
    id?: number
    first_name?: string | null
    last_name?: string | null
    company_name?: string | null
    email: string
    password_hash?: string | null
    phone?: string | null
    is_organizer?: boolean | null
    is_sponsor?: boolean | null
    is_vendor?: boolean | null
    is_admin?: boolean | null
    is_active?: boolean | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
  }

  export type UserCreateOrConnectWithoutEventsInput = {
    where: UserWhereUniqueInput
    create: XOR<UserCreateWithoutEventsInput, UserUncheckedCreateWithoutEventsInput>
  }

  export type VenueCreateWithoutEventsInput = {
    name?: string | null
    address?: string | null
    city?: string | null
    state?: string | null
    zip_code?: string | null
    latitude?: number | null
    longitude?: number | null
    capacity?: number | null
    venue_type_id?: number | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
  }

  export type VenueUncheckedCreateWithoutEventsInput = {
    id?: number
    name?: string | null
    address?: string | null
    city?: string | null
    state?: string | null
    zip_code?: string | null
    latitude?: number | null
    longitude?: number | null
    capacity?: number | null
    venue_type_id?: number | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
  }

  export type VenueCreateOrConnectWithoutEventsInput = {
    where: VenueWhereUniqueInput
    create: XOR<VenueCreateWithoutEventsInput, VenueUncheckedCreateWithoutEventsInput>
  }

  export type FunalyticsScoreCreateWithoutEventInput = {
    id?: string
    communityVibe?: number | null
    familyFun?: number | null
    overallScore?: number | null
    reasoning?: string | null
    computedAt?: Date | string
  }

  export type FunalyticsScoreUncheckedCreateWithoutEventInput = {
    id?: string
    communityVibe?: number | null
    familyFun?: number | null
    overallScore?: number | null
    reasoning?: string | null
    computedAt?: Date | string
  }

  export type FunalyticsScoreCreateOrConnectWithoutEventInput = {
    where: FunalyticsScoreWhereUniqueInput
    create: XOR<FunalyticsScoreCreateWithoutEventInput, FunalyticsScoreUncheckedCreateWithoutEventInput>
  }

  export type FunalyticsScoreCreateManyEventInputEnvelope = {
    data: FunalyticsScoreCreateManyEventInput | FunalyticsScoreCreateManyEventInput[]
    skipDuplicates?: boolean
  }

  export type UserUpsertWithoutEventsInput = {
    update: XOR<UserUpdateWithoutEventsInput, UserUncheckedUpdateWithoutEventsInput>
    create: XOR<UserCreateWithoutEventsInput, UserUncheckedCreateWithoutEventsInput>
    where?: UserWhereInput
  }

  export type UserUpdateToOneWithWhereWithoutEventsInput = {
    where?: UserWhereInput
    data: XOR<UserUpdateWithoutEventsInput, UserUncheckedUpdateWithoutEventsInput>
  }

  export type UserUpdateWithoutEventsInput = {
    first_name?: NullableStringFieldUpdateOperationsInput | string | null
    last_name?: NullableStringFieldUpdateOperationsInput | string | null
    company_name?: NullableStringFieldUpdateOperationsInput | string | null
    email?: StringFieldUpdateOperationsInput | string
    password_hash?: NullableStringFieldUpdateOperationsInput | string | null
    phone?: NullableStringFieldUpdateOperationsInput | string | null
    is_organizer?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_sponsor?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_vendor?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_admin?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_active?: NullableBoolFieldUpdateOperationsInput | boolean | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
  }

  export type UserUncheckedUpdateWithoutEventsInput = {
    id?: IntFieldUpdateOperationsInput | number
    first_name?: NullableStringFieldUpdateOperationsInput | string | null
    last_name?: NullableStringFieldUpdateOperationsInput | string | null
    company_name?: NullableStringFieldUpdateOperationsInput | string | null
    email?: StringFieldUpdateOperationsInput | string
    password_hash?: NullableStringFieldUpdateOperationsInput | string | null
    phone?: NullableStringFieldUpdateOperationsInput | string | null
    is_organizer?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_sponsor?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_vendor?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_admin?: NullableBoolFieldUpdateOperationsInput | boolean | null
    is_active?: NullableBoolFieldUpdateOperationsInput | boolean | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
  }

  export type VenueUpsertWithoutEventsInput = {
    update: XOR<VenueUpdateWithoutEventsInput, VenueUncheckedUpdateWithoutEventsInput>
    create: XOR<VenueCreateWithoutEventsInput, VenueUncheckedCreateWithoutEventsInput>
    where?: VenueWhereInput
  }

  export type VenueUpdateToOneWithWhereWithoutEventsInput = {
    where?: VenueWhereInput
    data: XOR<VenueUpdateWithoutEventsInput, VenueUncheckedUpdateWithoutEventsInput>
  }

  export type VenueUpdateWithoutEventsInput = {
    name?: NullableStringFieldUpdateOperationsInput | string | null
    address?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zip_code?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    capacity?: NullableIntFieldUpdateOperationsInput | number | null
    venue_type_id?: NullableIntFieldUpdateOperationsInput | number | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
  }

  export type VenueUncheckedUpdateWithoutEventsInput = {
    id?: IntFieldUpdateOperationsInput | number
    name?: NullableStringFieldUpdateOperationsInput | string | null
    address?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zip_code?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    capacity?: NullableIntFieldUpdateOperationsInput | number | null
    venue_type_id?: NullableIntFieldUpdateOperationsInput | number | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
  }

  export type FunalyticsScoreUpsertWithWhereUniqueWithoutEventInput = {
    where: FunalyticsScoreWhereUniqueInput
    update: XOR<FunalyticsScoreUpdateWithoutEventInput, FunalyticsScoreUncheckedUpdateWithoutEventInput>
    create: XOR<FunalyticsScoreCreateWithoutEventInput, FunalyticsScoreUncheckedCreateWithoutEventInput>
  }

  export type FunalyticsScoreUpdateWithWhereUniqueWithoutEventInput = {
    where: FunalyticsScoreWhereUniqueInput
    data: XOR<FunalyticsScoreUpdateWithoutEventInput, FunalyticsScoreUncheckedUpdateWithoutEventInput>
  }

  export type FunalyticsScoreUpdateManyWithWhereWithoutEventInput = {
    where: FunalyticsScoreScalarWhereInput
    data: XOR<FunalyticsScoreUpdateManyMutationInput, FunalyticsScoreUncheckedUpdateManyWithoutEventInput>
  }

  export type FunalyticsScoreScalarWhereInput = {
    AND?: FunalyticsScoreScalarWhereInput | FunalyticsScoreScalarWhereInput[]
    OR?: FunalyticsScoreScalarWhereInput[]
    NOT?: FunalyticsScoreScalarWhereInput | FunalyticsScoreScalarWhereInput[]
    id?: StringFilter<"FunalyticsScore"> | string
    eventId?: IntFilter<"FunalyticsScore"> | number
    communityVibe?: IntNullableFilter<"FunalyticsScore"> | number | null
    familyFun?: IntNullableFilter<"FunalyticsScore"> | number | null
    overallScore?: IntNullableFilter<"FunalyticsScore"> | number | null
    reasoning?: StringNullableFilter<"FunalyticsScore"> | string | null
    computedAt?: DateTimeFilter<"FunalyticsScore"> | Date | string
  }

  export type EventCreateWithoutOrganizerInput = {
    title: string
    description?: string | null
    startTime: Date | string
    endTime?: Date | string | null
    location?: string | null
    city?: string | null
    state?: string | null
    zipCode?: string | null
    latitude?: number | null
    longitude?: number | null
    category?: string | null
    status?: string | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
    venue?: VenueCreateNestedOneWithoutEventsInput
    funalytics?: FunalyticsScoreCreateNestedManyWithoutEventInput
  }

  export type EventUncheckedCreateWithoutOrganizerInput = {
    id?: number
    title: string
    description?: string | null
    startTime: Date | string
    endTime?: Date | string | null
    location?: string | null
    city?: string | null
    state?: string | null
    zipCode?: string | null
    latitude?: number | null
    longitude?: number | null
    category?: string | null
    venueId?: number | null
    status?: string | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
    funalytics?: FunalyticsScoreUncheckedCreateNestedManyWithoutEventInput
  }

  export type EventCreateOrConnectWithoutOrganizerInput = {
    where: EventWhereUniqueInput
    create: XOR<EventCreateWithoutOrganizerInput, EventUncheckedCreateWithoutOrganizerInput>
  }

  export type EventCreateManyOrganizerInputEnvelope = {
    data: EventCreateManyOrganizerInput | EventCreateManyOrganizerInput[]
    skipDuplicates?: boolean
  }

  export type EventUpsertWithWhereUniqueWithoutOrganizerInput = {
    where: EventWhereUniqueInput
    update: XOR<EventUpdateWithoutOrganizerInput, EventUncheckedUpdateWithoutOrganizerInput>
    create: XOR<EventCreateWithoutOrganizerInput, EventUncheckedCreateWithoutOrganizerInput>
  }

  export type EventUpdateWithWhereUniqueWithoutOrganizerInput = {
    where: EventWhereUniqueInput
    data: XOR<EventUpdateWithoutOrganizerInput, EventUncheckedUpdateWithoutOrganizerInput>
  }

  export type EventUpdateManyWithWhereWithoutOrganizerInput = {
    where: EventScalarWhereInput
    data: XOR<EventUpdateManyMutationInput, EventUncheckedUpdateManyWithoutOrganizerInput>
  }

  export type EventScalarWhereInput = {
    AND?: EventScalarWhereInput | EventScalarWhereInput[]
    OR?: EventScalarWhereInput[]
    NOT?: EventScalarWhereInput | EventScalarWhereInput[]
    id?: IntFilter<"Event"> | number
    title?: StringFilter<"Event"> | string
    description?: StringNullableFilter<"Event"> | string | null
    startTime?: DateTimeFilter<"Event"> | Date | string
    endTime?: DateTimeNullableFilter<"Event"> | Date | string | null
    location?: StringNullableFilter<"Event"> | string | null
    city?: StringNullableFilter<"Event"> | string | null
    state?: StringNullableFilter<"Event"> | string | null
    zipCode?: StringNullableFilter<"Event"> | string | null
    latitude?: FloatNullableFilter<"Event"> | number | null
    longitude?: FloatNullableFilter<"Event"> | number | null
    category?: StringNullableFilter<"Event"> | string | null
    organizerId?: IntNullableFilter<"Event"> | number | null
    venueId?: IntNullableFilter<"Event"> | number | null
    status?: StringNullableFilter<"Event"> | string | null
    created_at?: DateTimeNullableFilter<"Event"> | Date | string | null
    updated_at?: DateTimeNullableFilter<"Event"> | Date | string | null
  }

  export type EventCreateWithoutVenueInput = {
    title: string
    description?: string | null
    startTime: Date | string
    endTime?: Date | string | null
    location?: string | null
    city?: string | null
    state?: string | null
    zipCode?: string | null
    latitude?: number | null
    longitude?: number | null
    category?: string | null
    status?: string | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
    organizer?: UserCreateNestedOneWithoutEventsInput
    funalytics?: FunalyticsScoreCreateNestedManyWithoutEventInput
  }

  export type EventUncheckedCreateWithoutVenueInput = {
    id?: number
    title: string
    description?: string | null
    startTime: Date | string
    endTime?: Date | string | null
    location?: string | null
    city?: string | null
    state?: string | null
    zipCode?: string | null
    latitude?: number | null
    longitude?: number | null
    category?: string | null
    organizerId?: number | null
    status?: string | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
    funalytics?: FunalyticsScoreUncheckedCreateNestedManyWithoutEventInput
  }

  export type EventCreateOrConnectWithoutVenueInput = {
    where: EventWhereUniqueInput
    create: XOR<EventCreateWithoutVenueInput, EventUncheckedCreateWithoutVenueInput>
  }

  export type EventCreateManyVenueInputEnvelope = {
    data: EventCreateManyVenueInput | EventCreateManyVenueInput[]
    skipDuplicates?: boolean
  }

  export type EventUpsertWithWhereUniqueWithoutVenueInput = {
    where: EventWhereUniqueInput
    update: XOR<EventUpdateWithoutVenueInput, EventUncheckedUpdateWithoutVenueInput>
    create: XOR<EventCreateWithoutVenueInput, EventUncheckedCreateWithoutVenueInput>
  }

  export type EventUpdateWithWhereUniqueWithoutVenueInput = {
    where: EventWhereUniqueInput
    data: XOR<EventUpdateWithoutVenueInput, EventUncheckedUpdateWithoutVenueInput>
  }

  export type EventUpdateManyWithWhereWithoutVenueInput = {
    where: EventScalarWhereInput
    data: XOR<EventUpdateManyMutationInput, EventUncheckedUpdateManyWithoutVenueInput>
  }

  export type EventCreateWithoutFunalyticsInput = {
    title: string
    description?: string | null
    startTime: Date | string
    endTime?: Date | string | null
    location?: string | null
    city?: string | null
    state?: string | null
    zipCode?: string | null
    latitude?: number | null
    longitude?: number | null
    category?: string | null
    status?: string | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
    organizer?: UserCreateNestedOneWithoutEventsInput
    venue?: VenueCreateNestedOneWithoutEventsInput
  }

  export type EventUncheckedCreateWithoutFunalyticsInput = {
    id?: number
    title: string
    description?: string | null
    startTime: Date | string
    endTime?: Date | string | null
    location?: string | null
    city?: string | null
    state?: string | null
    zipCode?: string | null
    latitude?: number | null
    longitude?: number | null
    category?: string | null
    organizerId?: number | null
    venueId?: number | null
    status?: string | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
  }

  export type EventCreateOrConnectWithoutFunalyticsInput = {
    where: EventWhereUniqueInput
    create: XOR<EventCreateWithoutFunalyticsInput, EventUncheckedCreateWithoutFunalyticsInput>
  }

  export type EventUpsertWithoutFunalyticsInput = {
    update: XOR<EventUpdateWithoutFunalyticsInput, EventUncheckedUpdateWithoutFunalyticsInput>
    create: XOR<EventCreateWithoutFunalyticsInput, EventUncheckedCreateWithoutFunalyticsInput>
    where?: EventWhereInput
  }

  export type EventUpdateToOneWithWhereWithoutFunalyticsInput = {
    where?: EventWhereInput
    data: XOR<EventUpdateWithoutFunalyticsInput, EventUncheckedUpdateWithoutFunalyticsInput>
  }

  export type EventUpdateWithoutFunalyticsInput = {
    title?: StringFieldUpdateOperationsInput | string
    description?: NullableStringFieldUpdateOperationsInput | string | null
    startTime?: DateTimeFieldUpdateOperationsInput | Date | string
    endTime?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    location?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zipCode?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    category?: NullableStringFieldUpdateOperationsInput | string | null
    status?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    organizer?: UserUpdateOneWithoutEventsNestedInput
    venue?: VenueUpdateOneWithoutEventsNestedInput
  }

  export type EventUncheckedUpdateWithoutFunalyticsInput = {
    id?: IntFieldUpdateOperationsInput | number
    title?: StringFieldUpdateOperationsInput | string
    description?: NullableStringFieldUpdateOperationsInput | string | null
    startTime?: DateTimeFieldUpdateOperationsInput | Date | string
    endTime?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    location?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zipCode?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    category?: NullableStringFieldUpdateOperationsInput | string | null
    organizerId?: NullableIntFieldUpdateOperationsInput | number | null
    venueId?: NullableIntFieldUpdateOperationsInput | number | null
    status?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
  }

  export type FunalyticsScoreCreateManyEventInput = {
    id?: string
    communityVibe?: number | null
    familyFun?: number | null
    overallScore?: number | null
    reasoning?: string | null
    computedAt?: Date | string
  }

  export type FunalyticsScoreUpdateWithoutEventInput = {
    id?: StringFieldUpdateOperationsInput | string
    communityVibe?: NullableIntFieldUpdateOperationsInput | number | null
    familyFun?: NullableIntFieldUpdateOperationsInput | number | null
    overallScore?: NullableIntFieldUpdateOperationsInput | number | null
    reasoning?: NullableStringFieldUpdateOperationsInput | string | null
    computedAt?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type FunalyticsScoreUncheckedUpdateWithoutEventInput = {
    id?: StringFieldUpdateOperationsInput | string
    communityVibe?: NullableIntFieldUpdateOperationsInput | number | null
    familyFun?: NullableIntFieldUpdateOperationsInput | number | null
    overallScore?: NullableIntFieldUpdateOperationsInput | number | null
    reasoning?: NullableStringFieldUpdateOperationsInput | string | null
    computedAt?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type FunalyticsScoreUncheckedUpdateManyWithoutEventInput = {
    id?: StringFieldUpdateOperationsInput | string
    communityVibe?: NullableIntFieldUpdateOperationsInput | number | null
    familyFun?: NullableIntFieldUpdateOperationsInput | number | null
    overallScore?: NullableIntFieldUpdateOperationsInput | number | null
    reasoning?: NullableStringFieldUpdateOperationsInput | string | null
    computedAt?: DateTimeFieldUpdateOperationsInput | Date | string
  }

  export type EventCreateManyOrganizerInput = {
    id?: number
    title: string
    description?: string | null
    startTime: Date | string
    endTime?: Date | string | null
    location?: string | null
    city?: string | null
    state?: string | null
    zipCode?: string | null
    latitude?: number | null
    longitude?: number | null
    category?: string | null
    venueId?: number | null
    status?: string | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
  }

  export type EventUpdateWithoutOrganizerInput = {
    title?: StringFieldUpdateOperationsInput | string
    description?: NullableStringFieldUpdateOperationsInput | string | null
    startTime?: DateTimeFieldUpdateOperationsInput | Date | string
    endTime?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    location?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zipCode?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    category?: NullableStringFieldUpdateOperationsInput | string | null
    status?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    venue?: VenueUpdateOneWithoutEventsNestedInput
    funalytics?: FunalyticsScoreUpdateManyWithoutEventNestedInput
  }

  export type EventUncheckedUpdateWithoutOrganizerInput = {
    id?: IntFieldUpdateOperationsInput | number
    title?: StringFieldUpdateOperationsInput | string
    description?: NullableStringFieldUpdateOperationsInput | string | null
    startTime?: DateTimeFieldUpdateOperationsInput | Date | string
    endTime?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    location?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zipCode?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    category?: NullableStringFieldUpdateOperationsInput | string | null
    venueId?: NullableIntFieldUpdateOperationsInput | number | null
    status?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    funalytics?: FunalyticsScoreUncheckedUpdateManyWithoutEventNestedInput
  }

  export type EventUncheckedUpdateManyWithoutOrganizerInput = {
    id?: IntFieldUpdateOperationsInput | number
    title?: StringFieldUpdateOperationsInput | string
    description?: NullableStringFieldUpdateOperationsInput | string | null
    startTime?: DateTimeFieldUpdateOperationsInput | Date | string
    endTime?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    location?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zipCode?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    category?: NullableStringFieldUpdateOperationsInput | string | null
    venueId?: NullableIntFieldUpdateOperationsInput | number | null
    status?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
  }

  export type EventCreateManyVenueInput = {
    id?: number
    title: string
    description?: string | null
    startTime: Date | string
    endTime?: Date | string | null
    location?: string | null
    city?: string | null
    state?: string | null
    zipCode?: string | null
    latitude?: number | null
    longitude?: number | null
    category?: string | null
    organizerId?: number | null
    status?: string | null
    created_at?: Date | string | null
    updated_at?: Date | string | null
  }

  export type EventUpdateWithoutVenueInput = {
    title?: StringFieldUpdateOperationsInput | string
    description?: NullableStringFieldUpdateOperationsInput | string | null
    startTime?: DateTimeFieldUpdateOperationsInput | Date | string
    endTime?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    location?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zipCode?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    category?: NullableStringFieldUpdateOperationsInput | string | null
    status?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    organizer?: UserUpdateOneWithoutEventsNestedInput
    funalytics?: FunalyticsScoreUpdateManyWithoutEventNestedInput
  }

  export type EventUncheckedUpdateWithoutVenueInput = {
    id?: IntFieldUpdateOperationsInput | number
    title?: StringFieldUpdateOperationsInput | string
    description?: NullableStringFieldUpdateOperationsInput | string | null
    startTime?: DateTimeFieldUpdateOperationsInput | Date | string
    endTime?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    location?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zipCode?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    category?: NullableStringFieldUpdateOperationsInput | string | null
    organizerId?: NullableIntFieldUpdateOperationsInput | number | null
    status?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    funalytics?: FunalyticsScoreUncheckedUpdateManyWithoutEventNestedInput
  }

  export type EventUncheckedUpdateManyWithoutVenueInput = {
    id?: IntFieldUpdateOperationsInput | number
    title?: StringFieldUpdateOperationsInput | string
    description?: NullableStringFieldUpdateOperationsInput | string | null
    startTime?: DateTimeFieldUpdateOperationsInput | Date | string
    endTime?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    location?: NullableStringFieldUpdateOperationsInput | string | null
    city?: NullableStringFieldUpdateOperationsInput | string | null
    state?: NullableStringFieldUpdateOperationsInput | string | null
    zipCode?: NullableStringFieldUpdateOperationsInput | string | null
    latitude?: NullableFloatFieldUpdateOperationsInput | number | null
    longitude?: NullableFloatFieldUpdateOperationsInput | number | null
    category?: NullableStringFieldUpdateOperationsInput | string | null
    organizerId?: NullableIntFieldUpdateOperationsInput | number | null
    status?: NullableStringFieldUpdateOperationsInput | string | null
    created_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
    updated_at?: NullableDateTimeFieldUpdateOperationsInput | Date | string | null
  }



  /**
   * Batch Payload for updateMany & deleteMany & createMany
   */

  export type BatchPayload = {
    count: number
  }

  /**
   * DMMF
   */
  export const dmmf: runtime.BaseDMMF
}