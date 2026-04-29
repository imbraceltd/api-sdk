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
"vi/sdk/ai-agent.mdx": {
	id: "vi/sdk/ai-agent.mdx";
  slug: "vi/sdk/ai-agent";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/sdk/authentication.mdx": {
	id: "vi/sdk/authentication.mdx";
  slug: "vi/sdk/authentication";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/sdk/error-handling.mdx": {
	id: "vi/sdk/error-handling.mdx";
  slug: "vi/sdk/error-handling";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/sdk/full-flow-guide.mdx": {
	id: "vi/sdk/full-flow-guide.mdx";
  slug: "vi/sdk/full-flow-guide";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/sdk/installation.mdx": {
	id: "vi/sdk/installation.mdx";
  slug: "vi/sdk/installation";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/sdk/integrations.mdx": {
	id: "vi/sdk/integrations.mdx";
  slug: "vi/sdk/integrations";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/sdk/local-testing.mdx": {
	id: "vi/sdk/local-testing.mdx";
  slug: "vi/sdk/local-testing";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/sdk/overview.mdx": {
	id: "vi/sdk/overview.mdx";
  slug: "vi/sdk/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/sdk/quick-start.mdx": {
	id: "vi/sdk/quick-start.mdx";
  slug: "vi/sdk/quick-start";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"vi/sdk/resources.mdx": {
	id: "vi/sdk/resources.mdx";
  slug: "vi/sdk/resources";
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
"zh-cn/sdk/ai-agent.mdx": {
	id: "zh-cn/sdk/ai-agent.mdx";
  slug: "zh-cn/sdk/ai-agent";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/sdk/authentication.mdx": {
	id: "zh-cn/sdk/authentication.mdx";
  slug: "zh-cn/sdk/authentication";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/sdk/error-handling.mdx": {
	id: "zh-cn/sdk/error-handling.mdx";
  slug: "zh-cn/sdk/error-handling";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/sdk/full-flow-guide.mdx": {
	id: "zh-cn/sdk/full-flow-guide.mdx";
  slug: "zh-cn/sdk/full-flow-guide";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/sdk/installation.mdx": {
	id: "zh-cn/sdk/installation.mdx";
  slug: "zh-cn/sdk/installation";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/sdk/integrations.mdx": {
	id: "zh-cn/sdk/integrations.mdx";
  slug: "zh-cn/sdk/integrations";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/sdk/local-testing.mdx": {
	id: "zh-cn/sdk/local-testing.mdx";
  slug: "zh-cn/sdk/local-testing";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/sdk/overview.mdx": {
	id: "zh-cn/sdk/overview.mdx";
  slug: "zh-cn/sdk/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/sdk/quick-start.mdx": {
	id: "zh-cn/sdk/quick-start.mdx";
  slug: "zh-cn/sdk/quick-start";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-cn/sdk/resources.mdx": {
	id: "zh-cn/sdk/resources.mdx";
  slug: "zh-cn/sdk/resources";
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
"zh-tw/sdk/ai-agent.mdx": {
	id: "zh-tw/sdk/ai-agent.mdx";
  slug: "zh-tw/sdk/ai-agent";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/sdk/authentication.mdx": {
	id: "zh-tw/sdk/authentication.mdx";
  slug: "zh-tw/sdk/authentication";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/sdk/error-handling.mdx": {
	id: "zh-tw/sdk/error-handling.mdx";
  slug: "zh-tw/sdk/error-handling";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/sdk/full-flow-guide.mdx": {
	id: "zh-tw/sdk/full-flow-guide.mdx";
  slug: "zh-tw/sdk/full-flow-guide";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/sdk/installation.mdx": {
	id: "zh-tw/sdk/installation.mdx";
  slug: "zh-tw/sdk/installation";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/sdk/integrations.mdx": {
	id: "zh-tw/sdk/integrations.mdx";
  slug: "zh-tw/sdk/integrations";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/sdk/local-testing.mdx": {
	id: "zh-tw/sdk/local-testing.mdx";
  slug: "zh-tw/sdk/local-testing";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/sdk/overview.mdx": {
	id: "zh-tw/sdk/overview.mdx";
  slug: "zh-tw/sdk/overview";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/sdk/quick-start.mdx": {
	id: "zh-tw/sdk/quick-start.mdx";
  slug: "zh-tw/sdk/quick-start";
  body: string;
  collection: "docs";
  data: InferEntrySchema<"docs">
} & { render(): Render[".mdx"] };
"zh-tw/sdk/resources.mdx": {
	id: "zh-tw/sdk/resources.mdx";
  slug: "zh-tw/sdk/resources";
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
