type InfoCardProps = {
  title: string;
  children: React.ReactNode;
  label?: string;
};

export function InfoCard({ title, children, label }: InfoCardProps) {
  return (
    <section className="card">
      {label ? <span className="pill">{label}</span> : null}
      <h2>{title}</h2>
      <div>{children}</div>
    </section>
  );
}
