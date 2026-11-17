import HomePageComponentClient from "./ClientContactoPage";
async function page({ params }: { params: { slug: string } }) {
  // const paramsWait = await params;
  const { slug } = await params;
  console.log("Params: ",slug);
  // Consulta a la API o lógica para obtener los detalles del producto usando el ID
//   const product = PRODUCTOS_EJEMPLO.find(prod => prod.id.toString() === id) as ProductInterface;
  // const product = await productService.getById(paramsWait.id.toString());
  return (
    <HomePageComponentClient slug={slug} />
  )
}

export default page