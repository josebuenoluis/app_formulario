import HomePageComponentClient from "./ClientContactoPage";

export const instant = false;

async function page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;

  return <HomePageComponentClient slug={slug} />;
}

export default page;