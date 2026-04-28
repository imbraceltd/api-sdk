declare module 'astro:content' {
	interface Render {
		'.mdx': Promise<{
			Content: import('astro').MarkdownInstance<{}>['Content'];
			headings: import('astro').MarkdownHeading[];
			remarkPluginFrontmatter: Record<string, any>;
			components: import('astro').MDXInstance<{}>['components'];
		}>;
	}
}

declare module 'astro:content' {
	interface RenderResult {
		Content: import('astro/runtime/server/index.js').AstroComponentFactory;
		headings: import('astro').MarkdownHeading[];
		remarkPluginFrontmatter: Record<string, any>;
	}
	interface Render {
		'.md': Promise<RenderResult>;
	}

	export interface RenderedContent {
		html: string;
		metadata?: {
			imagePaths: Array<string>;
			[key: string]: unknown;
		};
	}
}

declare module 'astro:content' {
	type Flatten<T> = T extends { [K: string]: infer U } ? U : never;

	export type CollectionKey = keyof AnyEntryMap;
	export type CollectionEntry<C extends CollectionKey> = Flatten<AnyEntryMap[C]>;

	export type ContentCollectionKey = keyof ContentEntryMap;
	export type DataCollectionKey = keyof DataEntryMap;

	type AllValuesOf<T> = T extends any ? T[keyof T] : never;
	type ValidContentEntrySlug<C extends keyof ContentEntryMap> = AllValuesOf<
		ContentEntryMap[C]
	>['slug'];

	/** @deprecated Use `getEntry` instead. */
	export function getEntryBySlug<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(
		collection: C,
		// Note that this has to accept a regular string too, for SSR
		entrySlug: E,
	): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;

	/** @deprecated Use `getEntry` instead. */
	export function getDataEntryById<C extends keyof DataEntryMap, E extends keyof DataEntryMap[C]>(
		collection: C,
		entryId: E,
	): Promise<CollectionEntry<C>>;

	export function getCollection<C extends keyof AnyEntryMap, E extends CollectionEntry<C>>(
		collection: C,
		filter?: (entry: CollectionEntry<C>) => entry is E,
	): Promise<E[]>;
	export function getCollection<C extends keyof AnyEntryMap>(
		collection: C,
		filter?: (entry: CollectionEntry<C>) => unknown,
	): Promise<CollectionEntry<C>[]>;

	export function getEntry<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(entry: {
		collection: C;
		slug: E;
	}): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof DataEntryMap,
		E extends keyof DataEntryMap[C] | (string & {}),
	>(entry: {
		collection: C;
		id: E;
	}): E extends keyof DataEntryMap[C]
		? Promise<DataEntryMap[C][E]>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(
		collection: C,
		slug: E,
	): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof DataEntryMap,
		E extends keyof DataEntryMap[C] | (string & {}),
	>(
		collection: C,
		id: E,
	): E extends keyof DataEntryMap[C]
		? Promise<DataEntryMap[C][E]>
		: Promise<CollectionEntry<C> | undefined>;

	/** Resolve an array of entry references from the same collection */
	export function getEntries<C extends keyof ContentEntryMap>(
		entries: {
			collection: C;
			slug: ValidContentEntrySlug<C>;
		}[],
	): Promise<CollectionEntry<C>[]>;
	export function getEntries<C extends keyof DataEntryMap>(
		entries: {
			collection: C;
			id: keyof DataEntryMap[C];
		}[],
	): Promise<CollectionEntry<C>[]>;

	export function render<C extends keyof AnyEntryMap>(
		entry: AnyEntryMap[C][string],
	): Promise<RenderResult>;

	export function reference<C extends keyof AnyEntryMap>(
		collection: C,
	): import('astro/zod').ZodEffects<
		import('astro/zod').ZodString,
		C extends keyof ContentEntryMap
			? {
					collection: C;
					slug: ValidContentEntrySlug<C>;
				}
			: {
					collection: C;
					id: keyof DataEntryMap[C];
				}
	>;
	// Allow generic `string` to avoid excessive type errors in the config
	// if `dev` is not running to update as you edit.
	// Invalid collection names will be caught at build time.
	export function reference<C extends string>(
		collection: C,
	): import('astro/zod').ZodEffects<import('astro/zod').ZodString, never>;

	type ReturnTypeOrOriginal<T> = T extends (...args: any[]) => infer R ? R : T;
	type InferEntrySchema<C extends keyof AnyEntryMap> = import('astro/zod').infer<
		ReturnTypeOrOriginal<Required<ContentConfig['collections'][C]>['schema']>
	>;

	type ContentEntryMap = {
		"docs": {
"getting-started/overview.mdx": {
	id: "getting-started/overview.mdx";
  slug: "getting-started/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"getting-started/setup.mdx": {
	id: "getting-started/setup.mdx";
  slug: "getting-started/setup";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"guides/testing.mdx": {
	id: "guides/testing.mdx";
  slug: "guides/testing";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"guides/troubleshooting.mdx": {
	id: "guides/troubleshooting.mdx";
  slug: "guides/troubleshooting";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"index.mdx": {
	id: "index.mdx";
  slug: "index";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"python/ai-agent.mdx": {
	id: "python/ai-agent.mdx";
  slug: "python/ai-agent";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"python/authentication.mdx": {
	id: "python/authentication.mdx";
  slug: "python/authentication";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"python/error-handling.mdx": {
	id: "python/error-handling.mdx";
  slug: "python/error-handling";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"python/installation.mdx": {
	id: "python/installation.mdx";
  slug: "python/installation";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"python/integrations.mdx": {
	id: "python/integrations.mdx";
  slug: "python/integrations";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"python/overview.mdx": {
	id: "python/overview.mdx";
  slug: "python/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"python/quick-start.mdx": {
	id: "python/quick-start.mdx";
  slug: "python/quick-start";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"python/resources.mdx": {
	id: "python/resources.mdx";
  slug: "python/resources";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"typescript/ai-agent.mdx": {
	id: "typescript/ai-agent.mdx";
  slug: "typescript/ai-agent";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"typescript/authentication.mdx": {
	id: "typescript/authentication.mdx";
  slug: "typescript/authentication";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"typescript/error-handling.mdx": {
	id: "typescript/error-handling.mdx";
  slug: "typescript/error-handling";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"typescript/full-flow-guide.mdx": {
	id: "typescript/full-flow-guide.mdx";
  slug: "typescript/full-flow-guide";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"typescript/installation.mdx": {
	id: "typescript/installation.mdx";
  slug: "typescript/installation";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"typescript/integrations.mdx": {
	id: "typescript/integrations.mdx";
  slug: "typescript/integrations";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"typescript/local-testing.mdx": {
	id: "typescript/local-testing.mdx";
  slug: "typescript/local-testing";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"typescript/overview.mdx": {
	id: "typescript/overview.mdx";
  slug: "typescript/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"typescript/quick-start.mdx": {
	id: "typescript/quick-start.mdx";
  slug: "typescript/quick-start";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"typescript/resources.mdx": {
	id: "typescript/resources.mdx";
  slug: "typescript/resources";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/getting-started/overview.mdx": {
	id: "vi/getting-started/overview.mdx";
  slug: "vi/getting-started/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/getting-started/setup.mdx": {
	id: "vi/getting-started/setup.mdx";
  slug: "vi/getting-started/setup";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/guides/testing.mdx": {
	id: "vi/guides/testing.mdx";
  slug: "vi/guides/testing";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/guides/troubleshooting.mdx": {
	id: "vi/guides/troubleshooting.mdx";
  slug: "vi/guides/troubleshooting";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/index.mdx": {
	id: "vi/index.mdx";
  slug: "vi";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/python/ai-agent.mdx": {
	id: "vi/python/ai-agent.mdx";
  slug: "vi/python/ai-agent";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/python/authentication.mdx": {
	id: "vi/python/authentication.mdx";
  slug: "vi/python/authentication";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/python/error-handling.mdx": {
	id: "vi/python/error-handling.mdx";
  slug: "vi/python/error-handling";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/python/installation.mdx": {
	id: "vi/python/installation.mdx";
  slug: "vi/python/installation";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/python/integrations.mdx": {
	id: "vi/python/integrations.mdx";
  slug: "vi/python/integrations";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/python/overview.mdx": {
	id: "vi/python/overview.mdx";
  slug: "vi/python/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/python/quick-start.mdx": {
	id: "vi/python/quick-start.mdx";
  slug: "vi/python/quick-start";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/python/resources.mdx": {
	id: "vi/python/resources.mdx";
  slug: "vi/python/resources";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/typescript/ai-agent.mdx": {
	id: "vi/typescript/ai-agent.mdx";
  slug: "vi/typescript/ai-agent";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/typescript/authentication.mdx": {
	id: "vi/typescript/authentication.mdx";
  slug: "vi/typescript/authentication";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/typescript/error-handling.mdx": {
	id: "vi/typescript/error-handling.mdx";
  slug: "vi/typescript/error-handling";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/typescript/full-flow-guide.mdx": {
	id: "vi/typescript/full-flow-guide.mdx";
  slug: "vi/typescript/full-flow-guide";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/typescript/installation.mdx": {
	id: "vi/typescript/installation.mdx";
  slug: "vi/typescript/installation";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/typescript/integrations.mdx": {
	id: "vi/typescript/integrations.mdx";
  slug: "vi/typescript/integrations";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/typescript/local-testing.mdx": {
	id: "vi/typescript/local-testing.mdx";
  slug: "vi/typescript/local-testing";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/typescript/overview.mdx": {
	id: "vi/typescript/overview.mdx";
  slug: "vi/typescript/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/typescript/quick-start.mdx": {
	id: "vi/typescript/quick-start.mdx";
  slug: "vi/typescript/quick-start";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/typescript/resources.mdx": {
	id: "vi/typescript/resources.mdx";
  slug: "vi/typescript/resources";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/getting-started/overview.mdx": {
	id: "zh-cn/getting-started/overview.mdx";
  slug: "zh-cn/getting-started/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/getting-started/setup.mdx": {
	id: "zh-cn/getting-started/setup.mdx";
  slug: "zh-cn/getting-started/setup";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/guides/testing.mdx": {
	id: "zh-cn/guides/testing.mdx";
  slug: "zh-cn/guides/testing";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/guides/troubleshooting.mdx": {
	id: "zh-cn/guides/troubleshooting.mdx";
  slug: "zh-cn/guides/troubleshooting";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/index.mdx": {
	id: "zh-cn/index.mdx";
  slug: "zh-cn";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/python/ai-agent.mdx": {
	id: "zh-cn/python/ai-agent.mdx";
  slug: "zh-cn/python/ai-agent";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/python/authentication.mdx": {
	id: "zh-cn/python/authentication.mdx";
  slug: "zh-cn/python/authentication";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/python/error-handling.mdx": {
	id: "zh-cn/python/error-handling.mdx";
  slug: "zh-cn/python/error-handling";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/python/installation.mdx": {
	id: "zh-cn/python/installation.mdx";
  slug: "zh-cn/python/installation";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/python/integrations.mdx": {
	id: "zh-cn/python/integrations.mdx";
  slug: "zh-cn/python/integrations";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/python/overview.mdx": {
	id: "zh-cn/python/overview.mdx";
  slug: "zh-cn/python/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/python/quick-start.mdx": {
	id: "zh-cn/python/quick-start.mdx";
  slug: "zh-cn/python/quick-start";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/python/resources.mdx": {
	id: "zh-cn/python/resources.mdx";
  slug: "zh-cn/python/resources";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/typescript/ai-agent.mdx": {
	id: "zh-cn/typescript/ai-agent.mdx";
  slug: "zh-cn/typescript/ai-agent";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/typescript/authentication.mdx": {
	id: "zh-cn/typescript/authentication.mdx";
  slug: "zh-cn/typescript/authentication";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/typescript/error-handling.mdx": {
	id: "zh-cn/typescript/error-handling.mdx";
  slug: "zh-cn/typescript/error-handling";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/typescript/full-flow-guide.mdx": {
	id: "zh-cn/typescript/full-flow-guide.mdx";
  slug: "zh-cn/typescript/full-flow-guide";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/typescript/installation.mdx": {
	id: "zh-cn/typescript/installation.mdx";
  slug: "zh-cn/typescript/installation";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/typescript/integrations.mdx": {
	id: "zh-cn/typescript/integrations.mdx";
  slug: "zh-cn/typescript/integrations";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/typescript/local-testing.mdx": {
	id: "zh-cn/typescript/local-testing.mdx";
  slug: "zh-cn/typescript/local-testing";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/typescript/overview.mdx": {
	id: "zh-cn/typescript/overview.mdx";
  slug: "zh-cn/typescript/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/typescript/quick-start.mdx": {
	id: "zh-cn/typescript/quick-start.mdx";
  slug: "zh-cn/typescript/quick-start";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/typescript/resources.mdx": {
	id: "zh-cn/typescript/resources.mdx";
  slug: "zh-cn/typescript/resources";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/getting-started/overview.mdx": {
	id: "zh-tw/getting-started/overview.mdx";
  slug: "zh-tw/getting-started/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/getting-started/setup.mdx": {
	id: "zh-tw/getting-started/setup.mdx";
  slug: "zh-tw/getting-started/setup";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/guides/testing.mdx": {
	id: "zh-tw/guides/testing.mdx";
  slug: "zh-tw/guides/testing";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/guides/troubleshooting.mdx": {
	id: "zh-tw/guides/troubleshooting.mdx";
  slug: "zh-tw/guides/troubleshooting";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/index.mdx": {
	id: "zh-tw/index.mdx";
  slug: "zh-tw";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/python/ai-agent.mdx": {
	id: "zh-tw/python/ai-agent.mdx";
  slug: "zh-tw/python/ai-agent";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/python/authentication.mdx": {
	id: "zh-tw/python/authentication.mdx";
  slug: "zh-tw/python/authentication";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/python/error-handling.mdx": {
	id: "zh-tw/python/error-handling.mdx";
  slug: "zh-tw/python/error-handling";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/python/installation.mdx": {
	id: "zh-tw/python/installation.mdx";
  slug: "zh-tw/python/installation";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/python/integrations.mdx": {
	id: "zh-tw/python/integrations.mdx";
  slug: "zh-tw/python/integrations";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/python/overview.mdx": {
	id: "zh-tw/python/overview.mdx";
  slug: "zh-tw/python/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/python/quick-start.mdx": {
	id: "zh-tw/python/quick-start.mdx";
  slug: "zh-tw/python/quick-start";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/python/resources.mdx": {
	id: "zh-tw/python/resources.mdx";
  slug: "zh-tw/python/resources";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/typescript/ai-agent.mdx": {
	id: "zh-tw/typescript/ai-agent.mdx";
  slug: "zh-tw/typescript/ai-agent";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/typescript/authentication.mdx": {
	id: "zh-tw/typescript/authentication.mdx";
  slug: "zh-tw/typescript/authentication";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/typescript/error-handling.mdx": {
	id: "zh-tw/typescript/error-handling.mdx";
  slug: "zh-tw/typescript/error-handling";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/typescript/full-flow-guide.mdx": {
	id: "zh-tw/typescript/full-flow-guide.mdx";
  slug: "zh-tw/typescript/full-flow-guide";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/typescript/installation.mdx": {
	id: "zh-tw/typescript/installation.mdx";
  slug: "zh-tw/typescript/installation";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/typescript/integrations.mdx": {
	id: "zh-tw/typescript/integrations.mdx";
  slug: "zh-tw/typescript/integrations";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/typescript/local-testing.mdx": {
	id: "zh-tw/typescript/local-testing.mdx";
  slug: "zh-tw/typescript/local-testing";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/typescript/overview.mdx": {
	id: "zh-tw/typescript/overview.mdx";
  slug: "zh-tw/typescript/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/typescript/quick-start.mdx": {
	id: "zh-tw/typescript/quick-start.mdx";
  slug: "zh-tw/typescript/quick-start";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/typescript/resources.mdx": {
	id: "zh-tw/typescript/resources.mdx";
  slug: "zh-tw/typescript/resources";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
};

	};

	type DataEntryMap = {
		"i18n": {
"en": {
	id: "en";
  collection: "i18n";
  data: InferEntrySchema<"i18n">
};
"vi": {
	id: "vi";
  collection: "i18n";
  data: InferEntrySchema<"i18n">
};
"zh-cn": {
	id: "zh-cn";
  collection: "i18n";
  data: InferEntrySchema<"i18n">
};
"zh-tw": {
	id: "zh-tw";
  collection: "i18n";
  data: InferEntrySchema<"i18n">
};
};

	};

	type AnyEntryMap = ContentEntryMap & DataEntryMap;

	export type ContentConfig = typeof import("./../../src/content/config.js");
}
