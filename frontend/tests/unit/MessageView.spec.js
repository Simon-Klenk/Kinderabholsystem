import { shallowMount } from '@vue/test-utils';
import MessageCreate from '@/views/MessageView.vue';

jest.useFakeTimers();

describe('MessageCreate.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(MessageCreate);
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('renders the correct title', () => {
    expect(wrapper.find('h2.message-title').text()).toBe('Nachricht an AV senden');
  });

  it('displays Raspberry Pi online status correctly', async () => {
    await wrapper.setData({ isRaspberryOnline: true });
    expect(wrapper.find('.status-online').exists()).toBe(true);
    expect(wrapper.find('.status-offline').exists()).toBe(false);
  });

  it('displays Raspberry Pi offline status correctly', async () => {
    await wrapper.setData({ isRaspberryOnline: false });
    expect(wrapper.find('.status-online').exists()).toBe(false);
    expect(wrapper.find('.status-offline').exists()).toBe(true);
  });

  it('validates input correctly', async () => {
    const input = wrapper.find('input');
    await input.setValue('Max M.');
    await wrapper.vm.validateInput();
    expect(wrapper.vm.isValid).toBe(true);
  });

  it('displays an error message for invalid input', async () => {
    const input = wrapper.find('input');
    await input.setValue('Max Mustermann');
    await wrapper.vm.validateInput();
    expect(wrapper.vm.isValid).toBe(false);
    expect(wrapper.find('.error').text()).toContain("Bitte das Format 'Vorname N.' verwenden.");
  });

  it('disables the submit button if conditions are not met', async () => {
    await wrapper.setData({ isValid: false, isSubmitting: false, isRaspberryOnline: true });
    expect(wrapper.find('button').attributes('disabled')).toBeDefined();
  });

  it('enables the submit button when conditions are met', async () => {
    await wrapper.setData({ isValid: true, isSubmitting: false, isRaspberryOnline: true });
    expect(wrapper.find('button').attributes('disabled')).toBeUndefined();
  });
});
