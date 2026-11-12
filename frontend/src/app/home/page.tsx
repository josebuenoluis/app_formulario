"use client";

import React, { useState } from "react";

interface FormData {
  nombre: string;
  apellidos: string;
  prefijo: string;
  telefonoNumero: string;
  correo: string;
  producto_interes: "SALUD_DECESOS" | "SOLO_DECESOS";
  preguntas: string;
  aceptaPrivacidad: boolean;
}

export default function HomePageComponentClient() {
  const [formData, setFormData] = useState<FormData>({
    nombre: "",
    apellidos: "",
    prefijo: "+34",
    telefonoNumero: "",
    correo: "",
    producto_interes: "SALUD_DECESOS",
    preguntas: "",
    aceptaPrivacidad: false,
  });

  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState<string>("");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;

    if (type === "checkbox") {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData((prev) => ({ ...prev, [name]: checked }));
    } else if (name === "telefonoNumero") {
      const soloNumeros = value.replace(/\D/g, "");
      setFormData((prev) => ({ ...prev, [name]: soloNumeros }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");
    setErrorMessage("");

    const telefonoCompleto = `${formData.prefijo}${formData.telefonoNumero}`;

    if (formData.telefonoNumero.length < 9) {
      setStatus("error");
      setErrorMessage("Introduce un número de teléfono válido.");
      return;
    }

    const payload = {
      nombre: `${formData.nombre.trim()} ${formData.apellidos.trim()}`.trim(),
      telefono: telefonoCompleto,
      correo: formData.correo.trim(),
      producto_interes: formData.producto_interes,
      preguntas: formData.preguntas.trim(),
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/api/v1/contacto/enviar/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(
          errorData?.detail || "Error al procesar la solicitud. Revisa los datos."
        );
      }

      setStatus("success");
    } catch (err: unknown) {
      setStatus("error");
      setErrorMessage(
        err instanceof Error ? err.message : "Error de conexión con el servidor."
      );
    }
  };

  return (
    <div className="min-h-screen bg-white text-neutral-900 flex flex-col justify-between font-sans">
      {/* Cabecera minimalista */}
      <header className="border-b border-neutral-200 py-4 px-6 bg-white">
        <div className="max-w-5xl mx-auto flex justify-between items-center">
          <div className="font-extrabold text-xl tracking-tight text-neutral-900">
            BIENESTAR <span className="text-[#E51D53]">SALUD</span>
          </div>
          <span className="text-xs font-semibold text-[#E51D53]">
            Mejor precio garantizado
          </span>
        </div>
      </header>

      {/* Contenedor Principal */}
      <main className="max-w-5xl mx-auto w-full px-4 py-10 sm:py-14 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        
        {/* Columna Izquierda: Directa al grano */}
        <section className="lg:col-span-5 space-y-4">
          <p className="text-sm font-bold uppercase tracking-wider text-[#E51D53]">
            El mejor precio en el mercado.
          </p>

          <h1 className="text-4xl sm:text-5xl font-extrabold text-neutral-900 tracking-tight leading-tight">
            El mejor precio en bienestar salud.
          </h1>

          <ul className="pt-4 space-y-2.5 text-sm font-medium text-neutral-700">
            <li className="flex items-center gap-2.5">
              <span className="text-[#E51D53] font-bold">✓</span>
              Bienestar Salud (incluye Decesos)
            </li>
            <li className="flex items-center gap-2.5">
              <span className="text-[#E51D53] font-bold">✓</span>
              Solo Póliza de Decesos
            </li>
            <li className="flex items-center gap-2.5">
              <span className="text-[#E51D53] font-bold">✓</span>
              Respuesta inmediata por WhatsApp
            </li>
          </ul>
        </section>

        {/* Columna Derecha: Formulario limpio */}
        <section className="lg:col-span-7 max-w-md w-full mx-auto">
          <div className="bg-white rounded-2xl border border-neutral-300 shadow-sm p-6 sm:p-7">
            {status === "success" ? (
              <div className="text-center py-6 space-y-4">
                <div className="w-12 h-12 bg-rose-50 text-[#E51D53] rounded-full flex items-center justify-center mx-auto text-xl font-bold">
                  ✓
                </div>
                <h2 className="text-xl font-bold text-neutral-900">
                  ¡Solicitud recibida!
                </h2>
                <p className="text-sm text-neutral-600">
                  Te hemos enviado un WhatsApp al <strong>{formData.prefijo} {formData.telefonoNumero}</strong>.
                </p>
                <button
                  type="button"
                  onClick={() => {
                    setStatus("idle");
                    setFormData((prev) => ({ ...prev, preguntas: "" }));
                  }}
                  className="mt-2 w-full py-3 px-6 rounded-lg bg-[#E51D53] hover:bg-[#c91646] text-white font-semibold text-sm transition-colors cursor-pointer"
                >
                  Nueva consulta
                </button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <h2 className="text-lg font-bold text-neutral-900 pb-1">
                  Calcula tu tarifa
                </h2>

                {status === "error" && (
                  <div className="p-3 rounded-lg bg-rose-50 border border-[#E51D53] text-[#E51D53] text-xs font-medium">
                    {errorMessage}
                  </div>
                )}

                {/* Nombre y Apellidos agrupados */}
                <div className="rounded-lg border border-neutral-400 overflow-hidden focus-within:ring-2 focus-within:ring-neutral-900 focus-within:border-neutral-900 transition-all">
                  <div className="relative border-b border-neutral-400 px-3.5 pt-5 pb-1.5 bg-white">
                    <label
                      htmlFor="nombre"
                      className="absolute top-1.5 left-3.5 text-[11px] font-medium text-neutral-500"
                    >
                      Nombre
                    </label>
                    <input
                      id="nombre"
                      name="nombre"
                      type="text"
                      required
                      placeholder="Laura"
                      value={formData.nombre}
                      onChange={handleChange}
                      className="w-full text-sm text-neutral-900 placeholder-neutral-400 focus:outline-none bg-transparent"
                    />
                  </div>

                  <div className="relative px-3.5 pt-5 pb-1.5 bg-white">
                    <label
                      htmlFor="apellidos"
                      className="absolute top-1.5 left-3.5 text-[11px] font-medium text-neutral-500"
                    >
                      Apellidos
                    </label>
                    <input
                      id="apellidos"
                      name="apellidos"
                      type="text"
                      required
                      placeholder="García"
                      value={formData.apellidos}
                      onChange={handleChange}
                      className="w-full text-sm text-neutral-900 placeholder-neutral-400 focus:outline-none bg-transparent"
                    />
                  </div>
                </div>

                {/* Teléfono WhatsApp */}
                <div className="rounded-lg border border-neutral-400 overflow-hidden flex focus-within:ring-2 focus-within:ring-neutral-900 focus-within:border-neutral-900 transition-all bg-white">
                  <div className="relative border-r border-neutral-400 px-3 pt-5 pb-1.5 w-24 shrink-0 bg-neutral-50/60">
                    <label
                      htmlFor="prefijo"
                      className="absolute top-1.5 left-3 text-[11px] font-medium text-neutral-500"
                    >
                      Prefijo
                    </label>
                    <select
                      id="prefijo"
                      name="prefijo"
                      value={formData.prefijo}
                      onChange={handleChange}
                      className="w-full text-sm font-medium text-neutral-900 focus:outline-none bg-transparent cursor-pointer"
                    >
                      <option value="+34">+34</option>
                      <option value="+52">+52</option>
                      <option value="+57">+57</option>
                      <option value="+54">+54</option>
                      <option value="+56">+56</option>
                      <option value="+1">+1</option>
                    </select>
                  </div>

                  <div className="relative px-3.5 pt-5 pb-1.5 flex-1">
                    <label
                      htmlFor="telefonoNumero"
                      className="absolute top-1.5 left-3.5 text-[11px] font-medium text-neutral-500"
                    >
                      WhatsApp
                    </label>
                    <input
                      id="telefonoNumero"
                      name="telefonoNumero"
                      type="tel"
                      inputMode="numeric"
                      required
                      placeholder="600123456"
                      value={formData.telefonoNumero}
                      onChange={handleChange}
                      className="w-full text-sm text-neutral-900 placeholder-neutral-400 focus:outline-none bg-transparent"
                    />
                  </div>
                </div>

                {/* Correo electrónico */}
                <div className="relative rounded-lg border border-neutral-400 px-3.5 pt-5 pb-1.5 bg-white focus-within:ring-2 focus-within:ring-neutral-900 focus-within:border-neutral-900 transition-all">
                  <label
                    htmlFor="correo"
                    className="absolute top-1.5 left-3.5 text-[11px] font-medium text-neutral-500"
                  >
                    Correo electrónico
                  </label>
                  <input
                    id="correo"
                    name="correo"
                    type="email"
                    required
                    placeholder="laura@ejemplo.com"
                    value={formData.correo}
                    onChange={handleChange}
                    className="w-full text-sm text-neutral-900 placeholder-neutral-400 focus:outline-none bg-transparent"
                  />
                </div>

                {/* Producto a contratar */}
                <div className="relative rounded-lg border border-neutral-400 px-3.5 pt-5 pb-1.5 bg-white focus-within:ring-2 focus-within:ring-neutral-900 focus-within:border-neutral-900 transition-all">
                  <label
                    htmlFor="producto_interes"
                    className="absolute top-1.5 left-3.5 text-[11px] font-medium text-neutral-500"
                  >
                    Producto
                  </label>
                  <select
                    id="producto_interes"
                    name="producto_interes"
                    value={formData.producto_interes}
                    onChange={handleChange}
                    className="w-full text-sm text-neutral-900 focus:outline-none bg-transparent cursor-pointer"
                  >
                    <option value="SALUD_DECESOS">
                      Bienestar Salud (incluye Decesos)
                    </option>
                    <option value="SOLO_DECESOS">
                      Solo Póliza de Decesos
                    </option>
                  </select>
                </div>

                {/* Preguntas o dudas */}
                <div className="relative rounded-lg border border-neutral-400 px-3.5 pt-5 pb-1.5 bg-white focus-within:ring-2 focus-within:ring-neutral-900 focus-within:border-neutral-900 transition-all">
                  <label
                    htmlFor="preguntas"
                    className="absolute top-1.5 left-3.5 text-[11px] font-medium text-neutral-500"
                  >
                    Preguntas (opcional)
                  </label>
                  <textarea
                    id="preguntas"
                    name="preguntas"
                    rows={2}
                    placeholder="Escribe aquí tus dudas..."
                    value={formData.preguntas}
                    onChange={handleChange}
                    className="w-full text-sm text-neutral-900 placeholder-neutral-400 focus:outline-none bg-transparent resize-none"
                  />
                </div>

                {/* Checkbox obligatorio de privacidad */}
                <div className="flex items-start gap-2.5 pt-1">
                  <input
                    id="aceptaPrivacidad"
                    name="aceptaPrivacidad"
                    type="checkbox"
                    required
                    checked={formData.aceptaPrivacidad}
                    onChange={handleChange}
                    className="mt-0.5 h-4 w-4 rounded border-neutral-400 accent-[#E51D53] cursor-pointer shrink-0"
                  />
                  <label
                    htmlFor="aceptaPrivacidad"
                    className="text-xs text-neutral-600 leading-snug cursor-pointer"
                  >
                    Acepto la{" "}
                    <a
                      href="#privacidad"
                      className="underline font-medium text-neutral-900 hover:text-[#E51D53]"
                    >
                      Política de privacidad
                    </a>{" "}
                    y el contacto por WhatsApp. *
                  </label>
                </div>

                {/* Botón Principal */}
                <button
                  type="submit"
                  disabled={status === "loading"}
                  className="w-full py-3.5 px-6 rounded-lg bg-[#E51D53] hover:bg-[#c91646] disabled:bg-rose-300 text-white font-semibold text-sm tracking-wide transition-colors cursor-pointer"
                >
                  {status === "loading" ? "Enviando..." : "Aceptar y continuar"}
                </button>
              </form>
            )}
          </div>
        </section>
      </main>

      {/* Pie de página */}
      <footer className="border-t border-neutral-200 py-5 px-4 text-center text-xs text-neutral-400">
        © 2026 Bienestar Salud
      </footer>
    </div>
  );
}