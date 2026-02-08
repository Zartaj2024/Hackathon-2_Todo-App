export default function PrivacyPage() {
  return (
    <div className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Privacy Policy</h1>
        <div className="prose prose-gray max-w-none">
          <p className="text-gray-600">
            This is the privacy policy page for the Todo App.
          </p>

          <h2 className="text-xl font-semibold text-gray-900 mt-6">Information We Collect</h2>
          <p className="text-gray-600">
            We collect information you provide directly to us, such as when you create an account,
            update your profile, or use our services.
          </p>

          <h2 className="text-xl font-semibold text-gray-900 mt-6">How We Use Your Information</h2>
          <p className="text-gray-600">
            We use the information we collect to provide, maintain, and improve our services,
            and to communicate with you about your account and our services.
          </p>

          <h2 className="text-xl font-semibold text-gray-900 mt-6">Contact Us</h2>
          <p className="text-gray-600">
            If you have any questions about this Privacy Policy, please contact us.
          </p>
        </div>
      </div>
    </div>
  );
}